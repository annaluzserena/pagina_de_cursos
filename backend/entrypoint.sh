#!/bin/sh
# Exit immediately if a command exits with a non-zero status
set -e

echo "Running database migrations..."
uv run alembic upgrade head
echo "Running seed..."
uv run python -m app.seed --demo

echo "Starting application..."
# Executes whatever command is passed to the container (your CMD)
exec "$@"