#!/usr/bin/env bash
set -euo pipefail
echo "== Docker containers for project (filter by name 'agentic') =="
docker ps -a --filter "name=agentic" || true

echo "\n== Docker volumes =="
docker volume ls || true

echo "\n== Dangling volumes =="
docker volume ls -f dangling=true || true

echo "\nDone."
