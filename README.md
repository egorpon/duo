# Duo

Turn-based games for two players.

```
UI (React 19 :5173) -> API (FastAPI :8000) -> Auth gRPC (:50051)
                                           -> Game gRPC (:50052)
```

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- [just](https://github.com/casey/just)
- [pnpm](https://pnpm.io/)
- Docker + Docker Compose

## Setup

### 1. Install Python dependencies

```bash
uv sync
```

### 2. Copy environment files

Each service has an `.env.example` — copy them all:

```bash
# linux/mac
cp services/auth/.env.example services/auth/.env
cp services/game/.env.example services/game/.env
cp services/api/.env.example  services/api/.env
cp services/ui/.env.example   services/ui/.env
```

```powershell
# windows
copy services\auth\.env.example services\auth\.env
copy services\game\.env.example services\game\.env
copy services\api\.env.example  services\api\.env
copy services\ui\.env.example   services\ui\.env
```

Defaults should work for local development without modification.

### 3. Generate Ed25519 key pair

Auth issues JWT tokens with a private key; game and API verify with the public key.

```bash
python ./scripts/generate_key_pair_for_auth.py
```

This creates `ed25519` and `ed25519.pub` in the current directory. Distribute them:

```bash
# linux/mac — auth gets both keys
cp ed25519     services/auth/keys/ed25519
cp ed25519.pub services/auth/keys/ed25519.pub

# other services get public key only
cp ed25519.pub services/game/keys/ed25519.pub
cp ed25519.pub services/api/keys/ed25519.pub
```

```powershell
# windows
copy ed25519     services\auth\keys\ed25519
copy ed25519.pub services\auth\keys\ed25519.pub
copy ed25519.pub services\game\keys\ed25519.pub
copy ed25519.pub services\api\keys\ed25519.pub
```

Delete the root-level copies when done:

```bash
rm ed25519 ed25519.pub          # linux/mac
del ed25519 ed25519.pub         # windows
```

### 4. Generate gRPC code from proto files

```bash
just generate-proto
```

### 5. Start databases

```bash
docker compose up -d
```

Auth Postgres on `:25432`, Game Postgres on `:25433`.

### 6. Apply migrations

```bash
just apply-migrations auth
just apply-migrations game
```

### 7. Set up the UI

```bash
just ui install   # install pnpm dependencies
```

## Running

Open four terminals:

```bash
just run auth     # Auth gRPC service  :50051
just run game     # Game gRPC service  :50052
just run api      # FastAPI gateway    :8000
just ui dev       # React frontend     :5173
```

Open `http://localhost:5173`.

## Project layout

```
services/
  api/      REST gateway (FastAPI) — /api/v1/auth, /api/v1/users, /api/v1/games, /api/v1/ws
  auth/     gRPC UserService — JWT (Ed25519), Argon2 passwords, Postgres
  game/     gRPC GameService — game engine, Tic Tac Toe, Postgres
  ui/       React 19 + Vite + Zustand + TypeScript
common/     Shared Python utilities (logging, secrets, tokens)
proto/      Source .proto files (generated output → generated/)
scripts/    Developer utilities
```

## Development

```bash
just check          # format + type-check + test (run before committing)
just format         # ruff format + auto-fix
just type-check     # basedpyright strict
just test           # pytest
just test-cov       # pytest with coverage report

just ui run check   # format + lint + type-check for UI
```

Run a specific test directory:

```bash
pytest services/game/tests/tic_tac_toe/
```

Connect to a database:

```bash
just connect-to-db auth
just connect-to-db game
```
