#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

docker compose build
docker compose up -d

docker compose ps

RUNNING_SERVICES=$(docker compose ps --services --filter "status=running" | wc -l)

if [ "$RUNNING_SERVICES" -eq 3 ]; then
    echo "OK"
else
    echo "BŁĄD !!!"
    exit 1
fi