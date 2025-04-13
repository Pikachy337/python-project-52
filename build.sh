#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
set -o errexit

uv sync --all-packages

uv run python manage.py collectstatic --no-input

uv run python manage.py migrate