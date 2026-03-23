type-check:
	./.venv/bin/basedpyright
	./.venv/bin/mypy .


format:
	./.venv/bin/ruff format
	./.venv/bin/ruff check --fix


api:
	./.venv/bin/python -m services.api


auth:
	 ./.venv/bin/python -m services.auth


game:
	 ./.venv/bin/python -m services.game


ui:
	cd ./services/ui/; npm run dev


# copy .proto files inside generate so result files will have correct imports
generate-proto:
	cp proto/*.proto generated/
	./.venv/bin/python \
		-m grpc_tools.protoc \
		-I . \
		--python_out=. \
		--grpc_python_out=. \
		generated/*.proto
	rm generated/*.proto

test:
	 ./.venv/bin/pytest


auth-make-migrations:
	 ./.venv/bin/alembic \
		-c ./services/auth/alembic.ini revision --autogenerate


auth-apply-migrations:
	 ./.venv/bin/alembic \
		-c ./services/auth/alembic.ini upgrade head 


auth-connect-to-db:
	docker compose exec -it auth-postgres psql -U duo_auth -d duo_auth


game-make-migrations:
	 ./.venv/bin/alembic \
		-c ./services/game/alembic.ini revision --autogenerate


game-apply-migrations:
	 ./.venv/bin/alembic \
		-c ./services/game/alembic.ini upgrade head 


game-connect-to-db:
	docker compose exec -it game-postgres psql -U duo_game -d duo_game
