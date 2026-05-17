FROM python:3.14-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

RUN apt-get update && \
    apt-get install -y --no-install-recommends protobuf-compiler && \ 
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN uv sync --frozen --no-cache --group dev

RUN mkdir -p generated && \
    cp ./proto/*.proto ./generated/ && \
    uv run python -m grpc_tools.protoc -I . --python_out=. \
    --grpc_python_out=. ./generated/*.proto \
    && rm ./generated/*.proto

RUN uv sync --frozen --no-cache --no-group dev


FROM python:3.14-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

WORKDIR /app

COPY --from=builder /app /app

CMD ["sh"]
