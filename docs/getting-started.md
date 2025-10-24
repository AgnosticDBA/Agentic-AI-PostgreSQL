# Getting started — preview and deploy

Local preview

Install MkDocs and the Material theme (recommended):

```fish
pip install --user mkdocs mkdocs-material
# make sure $HOME/.local/bin is on your PATH or use the full path to the mkdocs executable
mkdocs serve
```

Open the URL shown (usually http://127.0.0.1:8000) to preview the site locally.

Deploy to GitHub Pages

If you'd like to publish to GitHub Pages, you can use MkDocs' gh-deploy command (it will build and push to the gh-pages branch):

```fish
mkdocs gh-deploy
```

Alternatively, use a GitHub Actions workflow to build and publish automatically on push. Ask me and I can add a simple `mkdocs.yml` GitHub Action that runs `mkdocs gh-deploy` on `main`.

Notes

- Keep the docs in `docs/` as plain Markdown so they are easy to edit and review.
- Do not place secrets in the docs; use the OS keychain or a secret manager for credentials.
