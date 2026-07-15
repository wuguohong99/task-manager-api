# syntax=docker/dockerfile:1

FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /install

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade \
        pip \
        setuptools \
        wheel \
    && python -m pip install \
        --prefix=/install \
        --no-cache-dir \
        -r requirements.txt


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8080 \
    LOG_LEVEL=INFO \
    RATE_LIMIT_PER_MINUTE=100

WORKDIR /app

RUN groupadd --system --gid 10001 app \
    && useradd \
        --system \
        --uid 10001 \
        --gid app \
        --home-dir /app \
        --shell /usr/sbin/nologin \
        app

COPY --from=builder /install /usr/local
COPY src ./src

# setuptools 和 wheel 只用于构建，生产运行时不需要
RUN python -m pip uninstall -y setuptools wheel \
    && rm -rf /root/.cache/pip \
    && chown -R 10001:10001 /app

USER 10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"PORT\", \"8080\")}/health', timeout=3).read()"

CMD ["sh", "-c", "exec uvicorn src.app:app --host ${HOST:-0.0.0.0} --port ${PORT:-8080}"]
