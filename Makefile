PYTHONPATH_SERVICES=services:generated

type-check:
	./.venv/bin/basedpyright
	./.venv/bin/mypy .


format:
	./.venv/bin/ruff format
	./.venv/bin/ruff check --fix


api:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/python -m services.api


auth:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/python -m services.auth


game:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/python -m services.game


ui:
	cd ./services/ui/; npm run dev


generate-proto:
	./.venv/bin/python \
		-m grpc_tools.protoc \
		-I proto \
		--python_out=generated \
		--grpc_python_out=generated \
		proto/*.proto

test:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/pytest


auth-make-migrations:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/alembic \
		-c ./services/auth/alembic.ini revision --autogenerate


auth-apply-migrations:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/alembic \
		-c ./services/auth/alembic.ini upgrade head 


auth-connect-to-db:
	docker compose exec -it auth-postgres psql -U duo_auth -d duo_auth


game-make-migrations:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/alembic \
		-c ./services/game/alembic.ini revision --autogenerate


game-apply-migrations:
	PYTHONPATH=$(PYTHONPATH_SERVICES) ./.venv/bin/alembic \
		-c ./services/game/alembic.ini upgrade head 


game-connect-to-db:
	docker compose exec -it game-postgres psql -U duo_game -d duo_game
