#!/usr/bin/env fish
# Quick environment & fish config checks for this project
printf "== Fish config checks ==\n"
if test -f $HOME/.config/fish/config.fish
    grep -n "pyenv\|zoxide\|secrets.fish" $HOME/.config/fish/config.fish 2>/dev/null || printf "No direct pyenv/zoxide/secrets references found in config.fish\n"
else
    printf "No ~/.config/fish/config.fish found\n"
end

printf "\nChecking presence of commands:\n"
for cmd in pyenv zoxide
    if type -q $cmd
        printf "%s: present\n" $cmd
    else
        printf "%s: missing\n" $cmd
    end
end

if test -f $HOME/.secrets.fish
    printf "\n~/.secrets.fish exists\n"
else
    printf "\n~/.secrets.fish missing\n"
end

printf "\n== Docker checks ==\n"
if type -q docker
    docker ps -a --filter name=agentic_pg16 --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}" 2>/dev/null || printf "(no agentic container found)\n"
    printf "\nVolumes:\n"
    docker volume ls 2>/dev/null | sed -n '1,200p'
else
    printf "docker not installed or not in PATH\n"
end

printf "\n== Git repo ==\n"
if type -q git
    git -C (pwd) rev-parse --show-toplevel 2>/dev/null || printf "no git repo detected at current path\n"
else
    printf "git not installed or not in PATH\n"
end

printf "\nDone.\n"
