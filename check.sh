#!/bin/sh
# Auto-fix lint and formatting issues, then run the tests.
set -e   # stop at the first failure

echo "🐍 Backend"
(cd backend && uv run ruff check --fix . && uv run ruff format . && uv run pytest -q)

echo "⚛️  Frontend"
(cd frontend && npm run lint -- --fix && npx prettier --write src)

echo "✅ All checks passed. Review the changes with git diff before committing."
