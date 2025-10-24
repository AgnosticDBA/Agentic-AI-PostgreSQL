# Architecture

This page summarizes the high-level architecture and key components used by the project.

Components

- Postgres (local dev): run via Docker Compose using `postgres:16-alpine`. Data is stored in a named Docker volume and initial SQL can be provided via `./initdb/`.
- Docker Compose: orchestrates the local Postgres service and mounts the `initdb/` directory for boot-time scripts.
- Notebooks: Jupyter notebooks live in `notebooks/`. Large, outputful notebooks are intentionally not tracked; templates are in `notebooks/templates/`.
- MkDocs: docs served from `docs/` and deployed to GitHub Pages via GitHub Actions.
- Pre-commit & nbstripout: repository is configured to strip notebook outputs and run common checks before commit.

Data & volumes

- The Postgres data volume is named using the compose project name (example: `agentic_pgdata`). Back up regularly if needed using `docker run --rm -v agentic_pgdata:/data -v $(pwd):/backup alpine sh -c "cd /data && tar czf /backup/pgdata-backup.tar.gz ."` (example approach).

Secrets & credentials

- Do not store secrets in the repo. Use OS keychain, 1Password, or a secret manager. GitHub Actions can access `secrets.GITHUB_TOKEN` for deployments; add any additional secrets in the repo settings.

Notes

- The project is intentionally lightweight for local development. If you later want to run Postgres in production, consider a managed provider or a secure VM with proper backups and monitoring.
