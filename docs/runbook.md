# Runbook: common tasks and troubleshooting

This runbook collects common commands and checks for local development with Docker Compose and the Postgres service.

Start / stop / status

```fish
# start in detached mode
docker compose up -d

# stop
docker compose down

# see container status
docker ps -a --filter name=agentic_pg16

# view logs
docker compose logs -f postgres
```

Database access

```fish
# connect from host using psql (example assumes pgcli/psql installed)
psql "host=127.0.0.1 port=5432 user=postgres dbname=postgres"
```

Backups

```fish
# export a SQL dump from the running container
docker exec -t $(docker compose ps -q postgres) pg_dumpall -U postgres > all.sql

# example restore
cat all.sql | docker exec -i $(docker compose ps -q postgres) psql -U postgres
```

Health checks & troubleshooting

- If `docker compose up` fails due to a container name conflict, inspect existing containers with `docker ps -a` and remove the conflicting container (if safe) with `docker rm -f <id>`.
- If volumes need cleaning, inspect `docker volume ls` and remove unused volumes carefully. Backup data before removing volumes.
- For fish startup issues (missing `pyenv` or `zoxide`), guard the configuration lines in `~/.config/fish/config.fish` with checks such as `if type -q pyenv;` or `if test -f ~/.secrets.fish; source ~/.secrets.fish; end`.

When to escalate

- If the DB data is corrupted or lost, restore from the most recent backup. Consider rotating backups and automated scheduled backups.
- For repeated container conflicts or orphaned networks, restart the Docker service or prune unused networks/volumes with care.
