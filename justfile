set dotenv-load := true

venv := "./.venv/bin"

check: format type-check test
    
# runs basedpyright
type-check:
    {{venv}}/basedpyright


lint:
    {{venv}}/ruff check


# formats code with ruff
format:
    {{venv}}/ruff format
    {{venv}}/ruff check --fix


test:
    {{venv}}/pytest

test-cov:
    {{venv}}/pytest --cov=services --cov-report=term-missing

# options: api, auth, game
run APP:
    {{venv}}/python -m services.{{APP}}


ui:
    cd ./services/ui/; npm run dev


generate-proto:
	cp ./proto/*.proto ./generated/
	{{venv}}/python \
		-m grpc_tools.protoc \
		-I . \
		--python_out=. \
		--grpc_python_out=. \
		--mypy_out=. \
		--mypy_grpc_out=. \
		./generated/*.proto
	rm ./generated/*.proto


# options: auth, game
make-migrations APP:
    {{venv}}/alembic -c ./services/{{APP}}/alembic.ini revision --autogenerate

# options: auth, game
apply-migrations APP:
    {{venv}}/alembic -c ./services/{{APP}}/alembic.ini upgrade head

# options: auth, game
rollback APP:
    {{venv}}/alembic -c ./services/{{APP}}/alembic.ini downgrade base


# options: auth, game
connect-to-db APP:
	docker compose exec -it {{APP}}-postgres psql -U duo_{{APP}} -d duo_{{APP}}


clean:
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -name "*.pyc" -delete
