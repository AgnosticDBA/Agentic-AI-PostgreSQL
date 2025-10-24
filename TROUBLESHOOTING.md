# Troubleshooting

This file collects quick checks and short explanations for common issues encountered while working with this project (fish shell startup problems, Docker/Compose issues, Git surprises, and Postgres checks).

## Fish startup errors (pyenv / zoxide / missing secrets)
- Symptom: `Unknown command: pyenv` or `zoxide`, or `source: No such file or directory` for `~/.secrets.fish`.
- Why: Your `~/.config/fish/config.fish` calls tools or sources files unconditionally that aren't installed or present.
- Quick check:
```fish
# show suspected lines with numbers
nl -ba ~/.config/fish/config.fish | sed -n '1,240p'
grep -n "pyenv\|zoxide\|secrets.fish" ~/.config/fish/config.fish
```
- Fix (safe pattern to add in `config.fish`):
```fish
if type -q pyenv
    set -gx PYENV_ROOT $HOME/.pyenv
    set -gx PATH $PYENV_ROOT/bin $PATH
    pyenv init - | source
end

if type -q zoxide
    zoxide init --cmd j fish | source
end

if test -f $HOME/.secrets.fish
    source $HOME/.secrets.fish
end
```

## Docker Compose container name conflicts
- Symptom: `Conflict. The container name "..." is already in use by container "..."` when running `docker compose up -d`.
- Why: A previous container still exists with the same `container_name` or Compose project name.
- Quick checks:
```fish
docker ps -a --filter name=agentic_pg16
docker inspect <container-id> --format '{{.Name}} {{.State.Status}}'
```
- Safe resolutions:
```fish
# If the container is safe to remove (stops DB service):
docker rm -f agentic_pg16
docker compose up -d

# If you want to remove stack and its volumes (destructive):
docker compose down --volumes
```
- Tip: avoid hardcoding `container_name` in `docker-compose.yml`. Use `COMPOSE_PROJECT_NAME` via a `.env` file or let Compose name containers.

## Docker volumes and data
- Question: was my DB data preserved?
- Quick checks:
```fish
docker inspect agentic_pg16 --format '{{json .Mounts}}'
docker volume inspect <volume-name>
docker volume ls -f dangling=true
```
- If you removed volumes with `docker compose down --volumes`, the named volume was deleted. To reclaim space, remove dangling volumes or run `docker volume prune`.

## Docker Compose warnings
- Example: `the attribute 'version' is obsolete` — harmless but noisy. Remove the top-level `version:` line from `docker-compose.yml` for modern Compose.

## Postgres healthchecks and connectivity
- Check the container health and readiness:
```fish
docker ps --filter name=agentic_pg16
docker logs agentic_pg16 --tail 100
docker exec -it agentic_pg16 pg_isready -U agentic -d agentic_db
# Or from host with psql (if psql is installed):
PGPASSWORD=agentic_pass psql -h localhost -p 5432 -U agentic -d agentic_db -c '\\l'
```

## Git and repository root surprises
- Symptom: `git` ignores or operates on your home directory instead of the project.
- Why: VS Code or your shell opened the home folder which is itself a Git repo.
- Quick check (from project dir):
```fish
git rev-parse --show-toplevel
git status --porcelain --untracked-files=all
```
- Fix: Initialize a repo inside the project directory (if not already a repo):
```fish
cd /path/to/Agentic-AI-PostgreSQL-Final
git init
git config user.name "Your Name"
git config user.email "you@example.com"
git add .
git commit -m "Initial commit"
```

## General safe troubleshooting checklist
- If a command fails, capture exact output and the last 10–20 lines of relevant logs (`docker logs`, shell error, or service log).
- Make backups before removing volumes or data. For Postgres, `pg_dump` or copying the volume data are options.
- Prefer guarded config entries for optional tools and files (shells, editors, CI) so missing tools don't break startup.

If you want, I can add short, machine-readable snippets for each of these checks (scripts) or expand the Postgres troubleshooting section with restore/backup commands.
