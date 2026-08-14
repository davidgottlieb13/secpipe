# ---- Stage 1: builder ----
# Installs dependencies into a user-local directory. Kept separate from the
# runtime stage so build tooling never ends up in the final image.
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Stage 2: runtime ----
# Minimal final image: only the interpreter, the installed dependencies,
# and the application code. Runs as a dedicated non-root user.
FROM python:3.12-slim

# Create a dedicated, unprivileged user rather than running as root (UID 0).
# A container running as root that gets compromised gives an attacker root
# inside the container by default — this closes that off cheaply.
RUN useradd --create-home --uid 1000 --shell /usr/sbin/nologin appuser

WORKDIR /app

# Copy only the installed packages from the builder stage, owned by appuser
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser main.py .

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

# Lightweight healthcheck using Python's stdlib only (no curl installed,
# keeps the image smaller)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
