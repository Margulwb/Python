#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building Docker images..."
docker compose build

echo "Starting services..."
docker compose up -d

echo "All services started. Use 'docker compose logs -f' to view logs."

sleep 5
echo "Checking the status of services..."

docker compose ps

# Sprawdzenie liczby uruchomionych serwisów
RUNNING_SERVICES=$(docker compose ps --services --filter "status=running" | wc -l)

if [ "$RUNNING_SERVICES" -eq 2 ]; then
    echo "OK: Są uruchomione dokładnie 2 serwisy."
else
    echo "BŁĄD: Liczba uruchomionych serwisów to $RUNNING_SERVICES (oczekiwano 2)."
    exit 1
fi