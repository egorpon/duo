venv := "./.venv/bin"


hello:
    echo "Empty just"

    
# runs basedpyright and mypy
type-check:
    {{venv}}/basedpyright
    {{venv}}/mypy .


# formats code with ruff
format:
    {{venv}}/ruff format
    {{venv}}/ruff check --fix


test:
    {{venv}}/pytest


# options: api, auth, game
run APP:
    {{venv}}/python -m services.{{APP}}


ui:
    cd ./services/ui/; npm run dev


generate-proto:
	cp proto/*.proto generated/
	{{venv}}/python \
		-m grpc_tools.protoc \
		-I . \
		--python_out=. \
		--grpc_python_out=. \
		generated/*.proto
	rm generated/*.proto


# options: auth, game
make-migrations APP:
    {{venv}}/alembic -c ./services/{{APP}}/alembic.ini revision --autogenerate

# options: auth, game
apply-migrations APP:
    {{venv}}/alembic -c ./services/{{APP}}/alembic.ini upgrade head


# options: auth, game
connect-to-db APP:
	docker compose exec -it {{APP}}-postgres psql -U duo_{{APP}} -d duo_{{APP}}
