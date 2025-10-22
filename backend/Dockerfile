# Builder stage - install dependencies
FROM python:3.13-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app
RUN pip install uv
RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock alembic.ini ./
COPY src/ ./src/
RUN uv sync --frozen

# Production stage
FROM python:3.13-slim AS prod

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app
RUN pip install uv
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY src/ ./src/
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "gamefleet_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]