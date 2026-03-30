#!/bin/bash

lsof -ti:8000 | xargs kill -9 2>/dev/null

cd "$(dirname "$0")"
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0
