# Tic-Tac-Toe

A full-stack tic-tac-toe game: a **React** frontend that talks to a **FastAPI** backend. The backend is the referee. It stores every game and enforces the rules, and the frontend only displays what the server says.

**Live:** [ttt-fe.onrender.com](https://ttt-fe.onrender.com) · API docs at [ttt-api-xj8k.onrender.com/docs](https://ttt-api-xj8k.onrender.com/docs)

> The backend runs on Render's free tier and sleeps after 15 minutes without traffic, so the first request after a quiet period can take up to a minute.

## Project layout

```
backend/     FastAPI app (Python, managed with uv)
  game.py      Game rules as pure functions: no web or database code
  main.py      HTTP API: routes, request/response models, CORS
  db.py        Database models and session setup (SQLModel)
  test_*.py    pytest tests for the rules and the API
frontend/    React app (Vite)
  src/         Components and styles (design tokens live in index.css)
.githooks/   Git hooks, version-controlled (see Setup)
check.sh     Lint, format, and test both apps
dev.sh       Run both dev servers at once
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (installs the right Python for you)
- [Node.js](https://nodejs.org/) and npm

## Setup

```bash
git clone https://github.com/aseem/tic-tac-toe.git
cd tic-tac-toe

# Turn on the pre-commit hook (local git config, so run this once per clone)
git config core.hooksPath .githooks

# Install dependencies
(cd backend && uv sync)
(cd frontend && npm install)
```

## Running locally

```bash
./dev.sh
```

This starts both servers. Press Ctrl+C to stop them both.

| | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

Locally, the backend stores games in a SQLite file, `backend/games.db`, which is created automatically and ignored by git.

## Checks and tests

```bash
./check.sh           # auto-fix lint and formatting, then run the tests
./check.sh --check   # only report problems, never change files
```

- **Backend:** ruff (lint and format) and pytest. API tests use a fresh in-memory database, so they never touch `games.db`.
- **Frontend:** oxlint and Prettier.

The **pre-commit hook** runs `./check.sh --check` before every commit and blocks the commit if anything fails. To fix the problems, run `./check.sh`, review the changes with `git diff`, `git add` them, and commit again.

**CI** (GitHub Actions, in `.github/workflows/ci.yml`) runs the same checks, plus a production frontend build, on every push to `main` and on every pull request.

## Configuration

Settings come from environment variables. Every one has a default that works locally, so you don't need to set anything for development.

| Variable | Service | Default | Purpose |
|---|---|---|---|
| `DATABASE_URL` | backend | `sqlite:///games.db` | Database connection. **Required on Render**, where it must be a `postgresql://` URL. The backend refuses to start without one. This URL contains a password: treat it as a secret. |
| `ALLOWED_ORIGINS` | backend | `http://localhost:5173` | Comma-separated frontend URLs allowed to call the API (CORS). No trailing slashes. |
| `VITE_API_URL` | frontend | `http://localhost:8000` | Backend URL. **Baked in at build time**, so changing it requires a rebuild. Public, never put secrets here. |

## Deployment

Both apps deploy to [Render](https://render.com) from this repo and redeploy automatically on push to `main`. To keep broken code from going live, set each service's **Auto-Deploy** option to wait for CI checks to pass.

| Service | Type | Root directory | Build command | Start command / publish directory |
|---|---|---|---|---|
| Backend | Web Service (Python) | `backend` | `uv sync --frozen` | `uv run fastapi run main.py --port $PORT` |
| Frontend | Static Site | `frontend` | `npm ci && npm run build` | `dist` |
| Database | Postgres | n/a | n/a | Backend uses its **Internal** Database URL |

> ⚠️ The free Render Postgres database **expires 30 days after creation**. When it does, create a new one (or move to a paid or different provider) and update `DATABASE_URL` on the backend. No code changes are needed.
