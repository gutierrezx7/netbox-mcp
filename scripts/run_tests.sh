#!/usr/bin/env bash
set -euo pipefail

echo "Installing dependencies..."
python -m pip install -r requirements.txt

echo "Running pytest..."
pytest -q
