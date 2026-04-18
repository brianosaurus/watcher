#!/usr/bin/env bash
set -euo pipefail
SSH_HOST="${SSH_HOST:-frankfurt}"
ssh "$SSH_HOST" "sudo systemctl restart watcher.service && sleep 1 && sudo systemctl status watcher.service --no-pager | head -10"
