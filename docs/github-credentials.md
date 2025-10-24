# GitHub credential options (kept for reference)

This file summarizes three common ways to authenticate with GitHub so you can push from this repository. Keep this file for future reference.

## A) SSH keys (recommended for long-term use)

When to use: you prefer SSH keys, want passwordless auth, or have multiple machines.

Steps (macOS / fish):

```fish
# generate a new ED25519 key (replace the email)
ssh-keygen -t ed25519 -C "your_email@example.com"

# start the agent (macOS comes with ssh-agent)
eval (ssh-agent -s)

# add the private key to the agent
ssh-add ~/.ssh/id_ed25519

# print the public key and copy it into GitHub > Settings > SSH and GPG keys
cat ~/.ssh/id_ed25519.pub
```

After adding the key to GitHub, add or update your remote to use the SSH URL:

```fish
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push -u origin HEAD
```

Notes:
- Use `ssh-agent` or macOS Keychain to avoid entering passphrases repeatedly.
- This is secure and widely recommended for developer machines.

## B) HTTPS with a Personal Access Token (PAT)

When to use: you can't/don't want to set up SSH keys, or you need fine-grained token scopes.

Steps:

1. Create a PAT at https://github.com/settings/tokens — choose scopes like `repo` (and `workflow` if needed).
2. Configure Git credential helper so macOS stores the token in Keychain:

```fish
git config --global credential.helper osxkeychain
```

3. Use the HTTPS remote URL. The first `git push` will prompt for credentials; use your username and the PAT as the password.

```fish
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin HEAD
```

Notes:
- PATs are easier if you need short-lived tokens or automation.
- Do NOT commit PATs or secrets to the repo. Use a secret manager (1Password, macOS Keychain, pass, etc.).

## C) GitHub CLI (`gh`) — interactive and convenient (you selected this)

When to use: you want a guided login flow, easy repo creation, and tight GitHub integration from the terminal. `gh` can create remotes, open PRs, and manage authentication.

Install (Homebrew):

```fish
brew install gh
```

Authenticate (interactive):

```fish
# web-based login (recommended interactive flow)
gh auth login --web

# or to force SSH protocol for git operations
gh auth login --web --git-protocol ssh

# check status
gh auth status
```

Create a GitHub repo (if you don't have one yet) and push the current directory:

```fish
# create a new repo under your user/org, add remote, and push
gh repo create YOUR_USERNAME/YOUR_REPO --public --source=. --remote=origin --push

# OR, if the repo already exists on GitHub, set remote and push
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push -u origin HEAD
```

Notes:
- `gh` will handle authentication (browser or device code) and can be used non-interactively with a token.
- Great for discoverability and automating repo tasks.

## Quick security reminders
- Never store PATs, private keys, or secrets in plain files in the repo.
- Use the OS keychain or a password manager for tokens.
- Limit token scopes to the minimum required.

---

If you'd like, I can now run the `gh` login flow interactively (it will open a browser) or provide exact commands to create the remote and push — tell me which account/repo name you want to use and whether you prefer SSH or HTTPS for the remote.
