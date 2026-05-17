FROM python:3.14-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

RUN apk add --no-cache protobuf-dev

WORKDIR /app

COPY . .

RUN uv sync --frozen --no-cache --no-group dev --group grpc

RUN mkdir -p generated && \
    cp ./proto/*.proto ./generated/ && \
    uv run python -m grpc_tools.protoc -I . --python_out=. \
    --grpc_python_out=. ./generated/*.proto \
    && rm ./generated/*.proto

RUN uv sync --frozen --no-cache --no-group dev --group production


FROM python:3.14-alpine

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

WORKDIR /app

COPY --from=builder /app /app

CMD ["sh"]
