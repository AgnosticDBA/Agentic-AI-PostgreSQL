Contributing and sharing
=======================

Thanks for considering sharing or contributing to this project. This file collects a few policies and steps to make collaboration smooth.

1) Keep templates clean
- Use the files under `notebooks/templates/` as starting points. Copy a template locally before running cells (`File -> Save As`) so you don't commit outputs.

2) Pre-commit hooks
- This repo uses `pre-commit` with `nbstripout` to automatically remove notebook outputs before commits. To enable locally:

```fish
# Install pre-commit (one-time)
pip install --user pre-commit

# From the repo root
pre-commit install
```

If `pre-commit` is not installed, follow the instructions above. After installation, hooks will run automatically on `git commit` and strip outputs from notebooks.

3) Notebooks
- Notebooks under `notebooks/` are intentionally not tracked (they may contain outputs). Use the `notebooks/templates/` versions for sharing.
- If you want to version a notebook, strip outputs first or rely on `pre-commit`.

4) Secrets and credentials
- Never commit secrets (API keys, passwords). Use `.env` (ignored) for per-machine overrides and keep credentials out of the repository.

5) How to share
- Create a fork or branch, make your changes, and open a PR. If you include runnable instructions, prefer small reproducible steps and avoid committing large binary outputs.

6) Running checks locally
- Quick checks: `scripts/check_env.fish` and `scripts/check_docker.sh` help verify environment and docker state.

If you want a different workflow (e.g., nbstripout disabled, or notebooks tracked via Git LFS), edit the `.pre-commit-config.yaml` and `.gitattributes` and coordinate with contributors.
