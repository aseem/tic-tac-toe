#!/usr/bin/env bash
# Start the backend and frontend dev servers together. Ctrl+C stops both.
#   Backend:  http://localhost:8000  (API docs at /docs)
#   Frontend: http://localhost:5173

# When this script exits for any reason, stop every process it started.
trap 'kill 0' EXIT

(cd backend && uv run fastapi dev main.py) &
(cd frontend && npm run dev) &

wait
