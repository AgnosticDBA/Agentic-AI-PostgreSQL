Agentic Local Bundle (Postgres 16)
==================================

How to use:
1. cd /path/to/agentic_local_bundle
2. docker compose up -d
3. python generate_data.py   # optionally pass --customers/--products/--orders/--metrics/--alerts/--logs
4. Install test deps: pip install -r requirements.txt
5. pytest -q tests

Notes:

Docker notes
------------

- This project uses `docker-compose.yml` to run Postgres locally. The compose stack maps Postgres to host port 5432 and uses a named volume for DB data.
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

CI / Automation
---------------

- This repository includes a GitHub Actions workflow that runs `pre-commit` hooks on pushes and pull requests. Once you push this repository to GitHub, the workflow will run automatically.

Badge (placeholder)
-------------------

If you add a GitHub remote named `origin`, you can include a status badge showing the workflow status. Replace `<owner>` and `<repo>` in the badge URL below with your GitHub username/org and repository name after pushing:

```
[![pre-commit](https://github.com/<owner>/<repo>/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/pre-commit.yml)
```

After you push the repo and the workflow runs successfully, the badge will reflect the check status.
