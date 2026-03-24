FROM python:3.12-slim AS base

# -------------------------------
# Metadados da imagem (OCI Labels)
# -------------------------------
LABEL org.opencontainers.image.title="Jobs APP"
LABEL org.opencontainers.image.description="App para simular fila de processamento com Redis"
LABEL org.opencontainers.image.version="1.1.0"
LABEL org.opencontainers.image.authors="Antonio Anerão <anerao.junior@gmail.com>"
LABEL org.opencontainers.image.vendor="Antonio Anerão"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl ca-certificates \
        redis-tools \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip uv

COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock
RUN uv sync --frozen --no-dev

COPY src /app/src
COPY .env /app/.env

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
