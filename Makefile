# PYTHONPATH_SERVICES=services/api:services/users:services/billing
PYTHONPATH_SERVICES=services:generated

type-check:
	.venv/bin/basedpyright
	.venv/bin/mypy .


format:
	.venv/bin/ruff format
	.venv/bin/ruff check --fix


api:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/python -m services.api

auth:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/python -m services.auth


ui:
	cd ./services/ui/; npm run dev


generate-proto:
	./.venv/bin/python -m grpc_tools.protoc -I proto --python_out=generated --grpc_python_out=generated proto/*.proto

