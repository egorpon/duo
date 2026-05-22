FROM python:3.14-alpine
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

EXPOSE 8000

CMD ["echo", "no CMD"]
