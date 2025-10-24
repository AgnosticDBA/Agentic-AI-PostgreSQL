Docker notes
============

This project uses a small `docker-compose.yml` to run Postgres locally. The compose stack maps Postgres to host port 5432 and uses a named volume for DB data.

Container naming
----------------

- Container naming is configurable using `COMPOSE_PROJECT_NAME` in a `.env` file. The default `.env` provided sets `COMPOSE_PROJECT_NAME=agentic`, which results in a container name like `agentic_pg16`.
- To avoid name collisions across machines, edit `.env` or set `COMPOSE_PROJECT_NAME` in your environment before running `docker compose up -d`.
- The repository includes `.gitignore` with `.env` listed so per-machine overrides are not committed.

Quick commands
--------------

```fish
# Start the stack (creates .env-controlled names)
docker compose up -d

# Show the Postgres container (filter by name)
docker ps -a --filter name=agentic_pg16
```
