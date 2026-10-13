#!/bin/sh
# Lint, format, and test both apps.
#   ./check.sh          auto-fix what can be fixed, then run the tests
#   ./check.sh --check  only report problems, never change files (used by the pre-commit hook)
set -e   # stop at the first failure

if [ "$1" = "--check" ]; then
  RUFF_CHECK=""; RUFF_FORMAT="--check"; LINT=""; PRETTIER="--check"
else
  RUFF_CHECK="--fix"; RUFF_FORMAT=""; LINT="--fix"; PRETTIER="--write"
fi

echo "🐍 Backend"
(cd backend && uv run ruff check $RUFF_CHECK . && uv run ruff format $RUFF_FORMAT . && uv run pytest -q)

echo "⚛️  Frontend"
(cd frontend && npm run lint -- $LINT && npx prettier $PRETTIER src)

echo "✅ All checks passed."
