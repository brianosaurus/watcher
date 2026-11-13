#!/usr/bin/env bash
# One-time bootstrap: install nginx + certbot, seed basic-auth, issue LE cert,
# switch to HTTPS config, start watcher service.
# Requires BASIC_AUTH_USER and BASIC_AUTH_PASS in env.
set -euo pipefail

SSH_HOST="${SSH_HOST:-frankfurt}"
REMOTE_DIR="/home/ubuntu/watcher"
DOMAIN="${DOMAIN:-brian.biz}"
UNCLE_DOMAIN="${UNCLE_DOMAIN:-unclehq.org}"
EMAIL="${EMAIL:-me@brian.biz}"

: "${BASIC_AUTH_USER:?BASIC_AUTH_USER not set}"
: "${BASIC_AUTH_PASS:?BASIC_AUTH_PASS not set}"

echo "▶ Installing nginx + certbot + apache2-utils"
ssh "$SSH_HOST" 'sudo DEBIAN_FRONTEND=noninteractive apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nginx certbot python3-certbot-nginx apache2-utils'

echo "▶ Seeding /etc/nginx/.htpasswd for user: ${BASIC_AUTH_USER}"
ssh "$SSH_HOST" "sudo htpasswd -bc /etc/nginx/.htpasswd $(printf %q "$BASIC_AUTH_USER") $(printf %q "$BASIC_AUTH_PASS") && sudo chmod 640 /etc/nginx/.htpasswd && sudo chown root:www-data /etc/nginx/.htpasswd"

echo "▶ Disabling default vhost and installing HTTP-only placeholder (for ACME)"
ssh "$SSH_HOST" "sudo rm -f /etc/nginx/sites-enabled/default && sudo cp ${REMOTE_DIR}/deploy/nginx-brian.biz-http-only.conf /etc/nginx/sites-available/brian.biz && sudo ln -sf /etc/nginx/sites-available/brian.biz /etc/nginx/sites-enabled/brian.biz && sudo mkdir -p /var/www/html && sudo nginx -t && sudo systemctl reload nginx"

echo "▶ Requesting Let's Encrypt cert for ${DOMAIN}"
ssh "$SSH_HOST" "sudo certbot certonly --webroot -w /var/www/html -d ${DOMAIN} -d www.${DOMAIN} --non-interactive --agree-tos -m ${EMAIL}"

echo "▶ Requesting Let's Encrypt cert for ${UNCLE_DOMAIN}"
# Fail closed: set -e aborts here on certbot failure, before any vhost install or reload.
ssh "$SSH_HOST" "sudo certbot certonly --webroot -w /var/www/html -d ${UNCLE_DOMAIN} -d www.${UNCLE_DOMAIN} --non-interactive --agree-tos -m ${EMAIL}"

echo "▶ Swapping to HTTPS nginx configs (brian.biz + ${UNCLE_DOMAIN})"
# Install only after both certs exist; restore prior configs and abort if nginx -t fails.
ssh "$SSH_HOST" "
  sudo test -f /etc/letsencrypt/live/${DOMAIN}/fullchain.pem &&
  sudo test -f /etc/letsencrypt/live/${UNCLE_DOMAIN}/fullchain.pem || { echo 'cert missing; aborting' >&2; exit 1; }
  for s in brian.biz ${UNCLE_DOMAIN}; do sudo cp -a /etc/nginx/sites-available/\$s /tmp/\$s.prev 2>/dev/null || true; done
  sudo cp ${REMOTE_DIR}/deploy/nginx-brian.biz.conf /etc/nginx/sites-available/brian.biz
  sudo cp ${REMOTE_DIR}/deploy/nginx-${UNCLE_DOMAIN}.conf /etc/nginx/sites-available/${UNCLE_DOMAIN}
  sudo ln -sf /etc/nginx/sites-available/${UNCLE_DOMAIN} /etc/nginx/sites-enabled/${UNCLE_DOMAIN}
  if ! sudo nginx -t; then
    echo 'nginx -t failed; restoring prior config, not reloading' >&2
    if [ -f /tmp/brian.biz.prev ]; then sudo cp /tmp/brian.biz.prev /etc/nginx/sites-available/brian.biz; fi
    sudo rm -f /etc/nginx/sites-enabled/${UNCLE_DOMAIN} /etc/nginx/sites-available/${UNCLE_DOMAIN}
    exit 1
  fi
  sudo systemctl reload nginx
"

echo "▶ Enabling + starting watcher service"
ssh "$SSH_HOST" "sudo systemctl enable --now watcher.service && sleep 2 && sudo systemctl status watcher.service --no-pager | head -15"

echo "✓ Bootstrap complete — https://${DOMAIN}"
