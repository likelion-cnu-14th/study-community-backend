#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
source "$SCRIPT_DIR/venv/bin/activate"

lsof -ti:8000 | xargs kill -9 2>/dev/null

uvicorn app.main:app --reload --host 0.0.0.0
