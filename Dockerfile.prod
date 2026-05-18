FROM python:3.14-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

RUN apk add --no-cache protobuf-dev

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-group dev --group grpc

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p generated && \
    cp ./proto/*.proto ./generated/ && \
    python -m grpc_tools.protoc -I . --python_out=. \
    --grpc_python_out=. ./generated/*.proto \
    && rm ./generated/*.proto

RUN uv sync --frozen --no-cache --no-group dev --group production --no-group grpc


FROM python:3.14-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/services /app/services
COPY --from=builder /app/common /app/common
COPY --from=builder /app/generated /app/generated


