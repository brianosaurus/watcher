#!/usr/bin/env bash
# Deploy watcher to Frankfurt. Idempotent: safe to re-run.
# Requires: BASIC_AUTH_USER, BASIC_AUTH_PASS in env (first run only, to seed .htpasswd).
set -euo pipefail

SSH_HOST="${SSH_HOST:-frankfurt}"
REMOTE_DIR="/home/ubuntu/watcher"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Build the React frontend (Vite) -> static/. static/ is generated (gitignored), so we
# always rebuild here to ship fresh, hash-named assets.
echo "▶ Building frontend (Vite → static/)"
( cd "$REPO_ROOT/frontend" && { [ -d node_modules ] || npm ci; } && npm run build )

echo "▶ Uploading code to ${SSH_HOST}:${REMOTE_DIR}"
ssh "$SSH_HOST" "mkdir -p ${REMOTE_DIR}"
# Only sync source files — never clobber anything outside REMOTE_DIR.
# COPYFILE_DISABLE suppresses macOS ._AppleDouble cruft in the tar stream.
# `rm -rf static/assets` first so stale hash-named bundles from past deploys don't pile up.
COPYFILE_DISABLE=1 tar czf - --no-xattrs -C "$REPO_ROOT" \
    app static requirements.txt deploy \
    | ssh "$SSH_HOST" "cd ${REMOTE_DIR} && rm -rf static/assets && tar xzf - && rm -f ._* app/._* static/._* deploy/._*"

# ~/venv's wrapper pip is misconfigured (wrong shebang) — always use python -m pip
echo "▶ Installing Python deps via ~/venv python -m pip"
ssh "$SSH_HOST" "~/venv/bin/python -m pip install -q -r ${REMOTE_DIR}/requirements.txt"

echo "▶ Installing systemd unit"
ssh "$SSH_HOST" "sudo cp ${REMOTE_DIR}/deploy/watcher.service /etc/systemd/system/watcher.service && sudo systemctl daemon-reload"

echo "✓ Code deployed. Next: run ./deploy/bootstrap-nginx.sh (first time) or ./deploy/restart.sh"
