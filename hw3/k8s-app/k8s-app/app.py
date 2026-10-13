"""
CMPE 789 - HW3 starter application.

A small HTTP service that serves a CPU-bound "market report" for a stock symbol.
The service works correctly as shipped, but it is deliberately slow. You will make
it fast in Part C without changing what it returns.

Endpoints:
  GET  /health              Liveness/readiness probe target.
  GET  /api/report?symbol=X The CPU-bound endpoint the load generator exercises.
  GET  /metrics             Request counters, cache counters, and the serving pod name.
  POST /admin/reset         Resets the counters. Requires the X-API-Token header.
"""

import os
import threading
import time

from flask import Flask, jsonify, request

app = Flask(__name__)

# Controls how much CPU work one report costs. Leave this alone: the graders run the
# default so that everyone's numbers are comparable.
WORK_FACTOR = int(os.environ.get("WORK_FACTOR", "60000"))

# Injected by the Kubernetes downward API (see k8s/deployment.yaml). Falls back to the
# hostname when you run the container directly with `docker run`.
POD_NAME = os.environ.get("POD_NAME", os.environ.get("HOSTNAME", "local"))

# Read from the environment so it can come from a Kubernetes Secret rather than from
# plaintext in a manifest. See Part B, Step 4.
API_TOKEN = os.environ.get("API_TOKEN", "")

STATS_LOCK = threading.Lock()
STATS = {"requests": 0, "cache_hits": 0, "cache_misses": 0}


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True


def _analyze(symbol: str) -> dict:
    """The expensive analysis. Deterministic: one symbol always yields one result.

    Do not modify this function. Part C is about avoiding unnecessary calls to it and
    about giving it enough CPU to run on, not about making the analysis itself cheaper.
    """
    seed = sum(ord(character) for character in symbol)
    window = WORK_FACTOR + (seed % 997)
    signal = sum(1 for candidate in range(2, window) if _is_prime(candidate))
    return {"symbol": symbol, "window": window, "signal": signal}


# ---------------------------------------------------------------------------
# TODO (HW3 Part C, Optimization 1): application-level caching
#
# compute_report() recomputes the full analysis on every single request, even when the
# same symbol was requested a millisecond ago. _analyze() is deterministic, so that
# work is pure waste whenever a symbol repeats.
#
# Implement an in-process cache:
#   1. On a cache hit, return the stored result WITHOUT calling _analyze() again.
#   2. On a cache miss, call _analyze(), store the result, and return it.
#   3. Increment STATS["cache_hits"] on a hit and STATS["cache_misses"] on a miss, so
#      that /metrics reports your hit rate. Hold STATS_LOCK while you mutate STATS.
#   4. Do not change the JSON schema returned by /api/report, and do not change
#      _analyze(). The report for a given symbol must stay byte-for-byte identical.
#
# The cache is per-process, so remember that each gunicorn worker and each pod replica
# keeps its own copy. Part C, Step 3 asks you to explain what that implies.
#
# A plain dict is enough here. Note that it is unbounded: a real in-memory cache such as
# Memcached is bounded and evicts under LRU. You do not have to implement eviction, but
# your report has to say what breaks without it.
# ---------------------------------------------------------------------------
Dict = {}

def compute_report(symbol: str) -> dict:
    with STATS_LOCK:
        if symbol in Dict:
            STATS["cache_hits"] += 1
            return Dict[symbol]
        else:
            STATS["cache_misses"] += 1

    analyze = _analyze(symbol)
    with STATS_LOCK:
        Dict[symbol] = analyze

    return analyze


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "pod": POD_NAME}), 200


@app.route("/api/report", methods=["GET"])
def report():
    symbol = request.args.get("symbol", "AAPL").strip().upper()
    if not symbol or not symbol.isalnum():
        return jsonify({"error": "symbol must be alphanumeric"}), 400

    with STATS_LOCK:
        STATS["requests"] += 1

    started = time.perf_counter()
    result = compute_report(symbol)
    compute_ms = (time.perf_counter() - started) * 1000.0

    return jsonify({**result, "compute_ms": round(compute_ms, 2), "pod": POD_NAME}), 200


@app.route("/metrics", methods=["GET"])
def metrics():
    with STATS_LOCK:
        snapshot = dict(STATS)

    lookups = snapshot["cache_hits"] + snapshot["cache_misses"]
    hit_rate = snapshot["cache_hits"] / lookups if lookups else 0.0

    return jsonify({**snapshot, "cache_hit_rate": round(hit_rate, 4), "pod": POD_NAME}), 200


@app.route("/admin/reset", methods=["POST"])
def reset():
    if not API_TOKEN or request.headers.get("X-API-Token") != API_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    with STATS_LOCK:
        for key in STATS:
            STATS[key] = 0

    return jsonify({"status": "reset", "pod": POD_NAME}), 200


if __name__ == "__main__":
    # Local convenience only. The container image serves the app with gunicorn; see the
    # Dockerfile. Never ship the Flask development server to a cloud environment.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False)
