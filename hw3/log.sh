#!/usr/bin/env bash
# Evidence logger for HW3. Copy this file to hw3/log.sh and run it from anywhere.
#
#   ./log.sh b2-local "docker build -t report-api:v1 k8s-app"
#   ./log.sh b2-local "curl -s localhost:8080/api/report"     # same name = appended
#   ./log.sh check                                            # are all 11 logs present?
#
# Each call appends a timestamp, the exact command, its full output and its exit
# code to logs/<name>.txt (next to this script) and also prints it to your screen.
# Quote the whole command so pipes and && stay inside it.
# Any value in $API_TOKEN (and its base64 form, which is how `kubectl get secret -o yaml`
# prints it) is replaced with <REDACTED> before it is written.
# Each call runs in a fresh shell, so `cd` does not carry over: write "cd k8s-app && docker build ...".
# Do not wrap commands that never finish (`docker run` without -d, `kubectl get pods -w`,
# `kubectl port-forward`); run those in another terminal and log the commands you run against them.
# Exit status: log.sh exits with the wrapped command's exit code, and `check` exits 1 if a log is missing.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
LOGS="$DIR/logs"; mkdir -p "$LOGS"
NEEDED="b1-versions b2-local b3-kind b3-gke b3-cleanup b4-hardening c1-baseline-hot c1-baseline-unique c2-pods c3-optimized-hot c3-optimized-unique"

if [ "${1:-}" = "check" ]; then
  bad=0
  for n in $NEEDED; do
    f="$LOGS/$n.txt"
    if [ ! -s "$f" ]; then echo "MISSING  $n.txt"; bad=1
    elif grep -q '^\[exit code: [1-9]' "$f"; then echo "ok       $n.txt   (contains a command that exited non-zero; fine if expected)"
    else echo "ok       $n.txt"; fi
  done
  exit $bad
fi

[ $# -ge 2 ] || { echo "usage: $0 <log-name> \"<command>\"   |   $0 check"; exit 2; }
name="$1"; shift
redact() {
  python3 -c '
import sys, os, base64
t = os.environ.get("API_TOKEN", "")
pats = [t, base64.b64encode(t.encode()).decode()] if t else []
for line in sys.stdin:
    for p in pats:
        line = line.replace(p, "<REDACTED>")
    sys.stdout.write(line)
'
}
{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
  echo "\$ $*"
  bash -c "$*" 2>&1
  rc=$?
  echo "[exit code: $rc]"
  echo
  exit $rc
} | redact | tee -a "$LOGS/$name.txt"
exit "${PIPESTATUS[0]}"
