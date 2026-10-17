#!/usr/bin/env bash
# Quick launcher for NeuroHive development environment
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
VENV_PYTHON="$DIR/.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Virtual environment not found. Initializing..."
    python3 -m venv --system-site-packages "$DIR/.venv"
fi

exec "$VENV_PYTHON" -m neurohive "$@"
