FROM python:3.14-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.11.14 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends protobuf-compiler && rm -rf /var/lib/apt/lists/*

RUN uv sync --frozen --no-cache --group dev

RUN mkdir -p generated && \
    cp ./proto/*.proto ./generated/ && \
    uv run python -m grpc_tools.protoc -I . --python_out=. \
    --grpc_python_out=. ./generated/*.proto \
    && rm ./generated/*.proto

ENV PATH="/app/.venv/bin:$PATH"

RUN uv sync --frozen --no-cache --no-group dev

CMD ["sh"]
