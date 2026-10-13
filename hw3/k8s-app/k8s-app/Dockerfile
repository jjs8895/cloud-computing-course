FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# The image runs as a non-root user so that the Kubernetes securityContext you add in
# Part B, Step 4 (runAsNonRoot: true) can be satisfied.
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin appuser
USER 10001

EXPOSE 8080

# The gthread worker class is used so the server supports HTTP keep-alive. Leave
# --worker-class alone: gunicorn's default `sync` worker closes the TCP connection after
# every response, which would force the load generator to burn a new socket per request.
#
# ---------------------------------------------------------------------------
# TODO (HW3 Part C, Optimization 2): container-level concurrency
#
# One gunicorn worker means one request is served at a time. Every other in-flight
# request waits, no matter how many CPUs the container is allowed to use.
#
# Tune --workers to the CPU budget the pod actually gets. Read the note in HW3.md,
# Part C, Step 2 before you pick a number: adding workers WITHOUT raising the CPU limit
# in k8s/deployment.yaml will make your p95 latency worse, not better. The two knobs
# have to move together.
#
# --threads is a separate knob. Think about what the GIL does to threads running a
# CPU-bound function before you reach for it, and say what you concluded in your report.
# ---------------------------------------------------------------------------
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--worker-class", "gthread", "--workers", "2", "--threads", "2", "app:app"]
