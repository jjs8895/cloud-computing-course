#!/usr/bin/env python3
"""
CMPE 789 - HW3 load generator (provided; you do not need to modify this file).

Drives a fixed number of concurrent clients at /api/report for a fixed duration and
reports throughput, latency percentiles, error rate, and how many distinct pods served
the traffic. Uses only the Python standard library, so there is nothing to install.

The two load patterns are the point of the exercise. They stress different bottlenecks:

  --pattern hot     Cycles through a handful of symbols. Most requests repeat a symbol
                    that was just requested, so a correct cache serves them almost for
                    free. This pattern rewards Optimization 1.

  --pattern unique  Draws from a large symbol space, so almost every request is a cache
                    miss and must actually run the analysis. Caching barely helps here;
                    only real CPU capacity does. This pattern rewards Optimizations 2
                    and 3.

Run both patterns before and after you optimize. An optimization that improves one
pattern and not the other is not a bug in your work: it is the result you are being
asked to explain.

Examples:
  python3 loadgen.py --url http://localhost:30080 --pattern hot    --duration 30 --concurrency 10
  python3 loadgen.py --url http://localhost:30080 --pattern unique --duration 30 --concurrency 10
  python3 loadgen.py --url http://localhost:30080 --pattern hot --json-out results/baseline-hot.json
"""

import argparse
import http.client
import json
import os
import statistics
import string
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

# A small working set: with 8 symbols and any reasonable cache, the hit rate approaches
# 100% within the first second of the run.
HOT_SYMBOLS = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AMD"]

# A large working set: 17,576 distinct symbols. A whole run issues far fewer requests
# than that, so under this pattern nearly every request is a first-time lookup.
UNIQUE_SYMBOLS = [
    f"{a}{b}{c}"
    for a in string.ascii_uppercase
    for b in string.ascii_uppercase
    for c in string.ascii_uppercase
]


def symbols_for_worker(pattern, worker_index, concurrency):
    """Decide which symbols one simulated client requests.

    Under `hot`, every client shares the same small list, so clients constantly request
    symbols that another client just requested. That is what a cache feeds on.

    Under `unique`, the symbol space is split into disjoint slices, one per client. No
    two clients ever ask for the same symbol, and no client revisits a symbol until it
    has exhausted its slice, which a run of this length never does. Without that split,
    the clients would all walk the same sequence and keep re-requesting each other's
    symbols, which would look like a cache-friendly workload and defeat the point of
    the pattern.
    """
    if pattern == "hot":
        return HOT_SYMBOLS
    return UNIQUE_SYMBOLS[worker_index::concurrency]


class Recorder:
    """Thread-safe collector for per-request outcomes."""

    def __init__(self):
        self._lock = threading.Lock()
        self.latencies_ms = []
        self.errors = 0
        self.pods = set()
        self.status_counts = {}

    def record_success(self, latency_ms, pod, status):
        with self._lock:
            self.latencies_ms.append(latency_ms)
            if pod:
                self.pods.add(pod)
            self.status_counts[status] = self.status_counts.get(status, 0) + 1

    def record_error(self, reason):
        with self._lock:
            self.errors += 1
            self.status_counts[reason] = self.status_counts.get(reason, 0) + 1


def open_connection(parsed):
    if parsed.scheme == "https":
        return http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=30)
    return http.client.HTTPConnection(parsed.hostname, parsed.port or 80, timeout=30)


def worker(url, symbols, deadline, recorder, worker_index):
    """One simulated client: issues requests back to back until the deadline.

    Each client holds ONE connection open and reuses it, the way a real load generator
    (wrk, hey, k6) does. Opening a fresh TCP connection per request would mean tens of
    thousands of sockets stuck in TIME_WAIT once the service gets fast, the client would
    run out of ephemeral ports, and the run would collapse into connection errors that
    look like a server fault but are not. Reuse also keeps the TCP handshake out of the
    latency numbers, so what you measure is the application, not the network.
    """
    parsed = urlparse(url)
    base_path = parsed.path.rstrip("/")
    connection = open_connection(parsed)

    # Offsetting the start keeps clients that share a list (the `hot` pattern) from
    # marching in lockstep through it.
    position = worker_index

    try:
        while time.monotonic() < deadline:
            symbol = symbols[position % len(symbols)]
            position += 1

            started = time.perf_counter()
            try:
                connection.request("GET", f"{base_path}/api/report?symbol={symbol}")
                response = connection.getresponse()
                # The body must be read in full before the connection can be reused.
                body = response.read()
                latency_ms = (time.perf_counter() - started) * 1000.0

                if response.status != 200:
                    recorder.record_error(f"http_{response.status}")
                    continue

                pod = None
                try:
                    pod = json.loads(body).get("pod")
                except (ValueError, AttributeError):
                    pass
                recorder.record_success(latency_ms, pod, response.status)
            except (http.client.HTTPException, OSError, TimeoutError) as error:
                recorder.record_error(type(error).__name__)
                # The connection is in an unknown state; drop it and start a new one.
                connection.close()
                connection = open_connection(parsed)
    finally:
        connection.close()


def percentile(sorted_values, fraction):
    """Nearest-rank percentile. sorted_values must be non-empty and sorted ascending."""
    rank = max(1, int(round(fraction * len(sorted_values))))
    return sorted_values[min(rank, len(sorted_values)) - 1]


def fetch_metrics(url):
    """Best-effort read of the app's /metrics endpoint. Returns None if unavailable."""
    try:
        with urllib.request.urlopen(f"{url.rstrip('/')}/metrics", timeout=10) as response:
            return json.loads(response.read())
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, OSError, TimeoutError):
        return None


def cache_delta(before, after):
    """Cache hits/misses attributable to THIS run.

    The app's counters are cumulative for the life of the process, so reading /metrics
    only after the run would fold in every earlier run against the same pod. Running
    `hot` and then `unique` would then report a misleadingly high hit rate for `unique`.
    Differencing the counters around the run isolates this run's behavior.

    This is still only a sample: /metrics is answered by whichever pod and whichever
    gunicorn worker happened to receive the call, and each keeps its own counters.
    """
    if not before or not after:
        return None

    hits = after.get("cache_hits", 0) - before.get("cache_hits", 0)
    misses = after.get("cache_misses", 0) - before.get("cache_misses", 0)
    lookups = hits + misses

    # A negative delta means the pod restarted (or a different pod answered) mid-run.
    if lookups <= 0 or hits < 0 or misses < 0:
        return None

    return {
        "cache_hits": hits,
        "cache_misses": misses,
        "cache_hit_rate": round(hits / lookups, 4),
        "sampled_from_pod": after.get("pod"),
    }


def main():
    parser = argparse.ArgumentParser(description="HW3 load generator")
    parser.add_argument("--url", default="http://localhost:30080", help="Base URL of the service")
    parser.add_argument("--pattern", choices=["hot", "unique"], default="hot", help="Symbol access pattern")
    parser.add_argument("--duration", type=int, default=30, help="Run length in seconds")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent clients")
    parser.add_argument("--label", default="", help="Free-text label recorded in the JSON output")
    parser.add_argument("--json-out", default="", help="Write the results to this JSON file")
    args = parser.parse_args()

    if args.duration < 1:
        parser.error("--duration must be at least 1 second")
    if args.concurrency < 1:
        parser.error("--concurrency must be at least 1")

    symbol_space = len(HOT_SYMBOLS if args.pattern == "hot" else UNIQUE_SYMBOLS)

    print(f"Target       : {args.url}")
    print(f"Pattern      : {args.pattern} ({symbol_space} distinct symbols)")
    print(f"Duration     : {args.duration}s")
    print(f"Concurrency  : {args.concurrency}")
    print("Running...", flush=True)

    metrics_before = fetch_metrics(args.url)

    recorder = Recorder()
    started_at = time.monotonic()
    deadline = started_at + args.duration

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        for worker_index in range(args.concurrency):
            pool.submit(
                worker,
                args.url,
                symbols_for_worker(args.pattern, worker_index, args.concurrency),
                deadline,
                recorder,
                worker_index,
            )

    elapsed = time.monotonic() - started_at

    successes = len(recorder.latencies_ms)
    total = successes + recorder.errors

    if successes == 0:
        print("\nNo successful requests. Is the service reachable at the URL above?")
        print(f"Outcomes: {recorder.status_counts}")
        return 1

    latencies = sorted(recorder.latencies_ms)
    summary = {
        "label": args.label,
        "url": args.url,
        "pattern": args.pattern,
        "duration_s": round(elapsed, 2),
        "concurrency": args.concurrency,
        "requests_total": total,
        "requests_ok": successes,
        "requests_failed": recorder.errors,
        "error_rate_pct": round(100.0 * recorder.errors / total, 2) if total else 0.0,
        "throughput_rps": round(successes / elapsed, 2),
        "latency_ms": {
            "mean": round(statistics.fmean(latencies), 2),
            "p50": round(percentile(latencies, 0.50), 2),
            "p90": round(percentile(latencies, 0.90), 2),
            "p95": round(percentile(latencies, 0.95), 2),
            "p99": round(percentile(latencies, 0.99), 2),
            "max": round(latencies[-1], 2),
        },
        "distinct_pods_observed": sorted(recorder.pods),
        "outcomes": recorder.status_counts,
    }

    cache = cache_delta(metrics_before, fetch_metrics(args.url))
    if cache:
        summary["cache_sample"] = cache

    print()
    print("=" * 58)
    print(f"  RESULTS  ({args.pattern} pattern, {args.concurrency} clients)")
    print("=" * 58)
    print(f"  Throughput        : {summary['throughput_rps']:>10.2f} req/s")
    print(f"  Requests OK       : {summary['requests_ok']:>10}")
    print(f"  Requests failed   : {summary['requests_failed']:>10}  ({summary['error_rate_pct']}%)")
    print("  " + "-" * 54)
    print(f"  Latency mean      : {summary['latency_ms']['mean']:>10.2f} ms")
    print(f"  Latency p50       : {summary['latency_ms']['p50']:>10.2f} ms")
    print(f"  Latency p90       : {summary['latency_ms']['p90']:>10.2f} ms")
    print(f"  Latency p95       : {summary['latency_ms']['p95']:>10.2f} ms")
    print(f"  Latency p99       : {summary['latency_ms']['p99']:>10.2f} ms")
    print(f"  Latency max       : {summary['latency_ms']['max']:>10.2f} ms")
    print("  " + "-" * 54)
    print(f"  Pods observed     : {len(summary['distinct_pods_observed'])} "
          f"{summary['distinct_pods_observed']}")
    if cache:
        print(f"  Cache hit rate    : {cache['cache_hit_rate']:>10.4f}  "
              f"({cache['cache_hits']} hits / {cache['cache_misses']} misses, "
              f"sampled from pod {cache['sampled_from_pod']})")
    else:
        print("  Cache hit rate    :        n/a  (/metrics unreachable, or the "
              "sampled pod restarted mid-run)")
    print("=" * 58)

    if args.json_out:
        directory = os.path.dirname(args.json_out)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2)
        print(f"\nSaved results to {args.json_out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
