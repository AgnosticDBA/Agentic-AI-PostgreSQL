# Personal wiki and note-taking options (recommended approaches)

Short summary: choose between a private local-first vault (Obsidian / plain Markdown + git) or a web-hosted docs site (MkDocs / GitHub Pages / Docusaurus) depending on whether your notes are personal/private or meant to be shared.

Options and recommendations

1. Obsidian (local-first, powerful)
   - Pros: great editor, plugins, local-only, fast. Works offline. Can sync via git or Obsidian Sync.
   - Cons: desktop-first, some features are paid.
   - Workflow: keep a git repo for your vault (private), push to a private GitHub repo for backup.

2. MkDocs (static site, Git-backed, great for docs)
   - Pros: Markdown -> static site, easy GitHub Pages deployment, search and navigation.
   - Cons: slightly more setup, more formal structure.
   - Quick start:

```fish
pip install mkdocs mkdocs-material
mkdocs new my-docs
# edit docs/, mkdocs.yml, then
mkdocs serve    # local preview
mkdocs gh-deploy  # deploy to GitHub Pages
```

3. GitHub Wiki (repo-integrated)
   - Pros: built into GitHub, git-backed, quick for project docs.
   - Cons: less flexible than a docs site, lives in a separate git repo per project.

4. Notion / OneNote (cloud-hosted)
   - Pros: excellent search, collaboration, structured pages, sharing.
   - Cons: vendor lock-in, not Git-friendly, not plaintext-first.

5. TiddlyWiki (single-file wiki)
   - Pros: portable single-file wiki.
   - Cons: quirky editing workflow, less standard for developer docs.


Suggested minimal on-disk structure (git repo) for notes you want to keep with the project:

```
docs/                      # markdown docs that can be served by MkDocs or GH Pages
  01-projects/
  02-infra/
  03-credentials.md        # short summaries (no secrets)
templates/
notes/                     # personal notes (if public, avoid secrets)
```

Example page template (credentials / how-tos)

---
title: GitHub credentials
tags: [credentials, git]
---

# Summary

- Short summary of the method used (SSH, PAT, or gh)

# Commands

```fish
# example commands go here
```

# Security

- Where secrets are stored (password manager, Keychain, etc.)


Security & hygiene
- Never commit secrets. If you need to keep an encrypted secret in the repo, use a tool such as git-crypt or SOPS (GPG-based) and store keys outside the repo.
- Prefer OS keychain, 1Password, or pass for secrets.

Backup and sync guidance
- For personal vaults, use a private GitHub repo (or private cloud sync) as a backup; avoid exposing secrets.
- For team docs/public docs, prefer MkDocs/Docusaurus + GitHub Pages for a stable website.

Recommendation (short):
- For private personal notes: Obsidian + git sync to a private repo (or Obsidian Sync).
- For sharable project docs: `docs/` + MkDocs (material) and GitHub Pages.

Next steps I can help with
- Create a `docs/` skeleton (MkDocs) in this repo and add a sample page.
- Initialize an Obsidian-friendly repo layout and `.gitignore` entries.
- Help run `gh auth login` and create the GitHub remote and push.
