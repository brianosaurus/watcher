#!/usr/bin/env bash
# One-time bootstrap: install nginx + certbot, seed basic-auth, issue LE cert,
# switch to HTTPS config, start watcher service.
# Requires BASIC_AUTH_USER and BASIC_AUTH_PASS in env.
set -euo pipefail

SSH_HOST="${SSH_HOST:-frankfurt}"
REMOTE_DIR="/home/ubuntu/watcher"
DOMAIN="${DOMAIN:-brian.biz}"
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

echo "▶ Swapping to HTTPS nginx config"
ssh "$SSH_HOST" "sudo cp ${REMOTE_DIR}/deploy/nginx-brian.biz.conf /etc/nginx/sites-available/brian.biz && sudo nginx -t && sudo systemctl reload nginx"

echo "▶ Enabling + starting watcher service"
ssh "$SSH_HOST" "sudo systemctl enable --now watcher.service && sleep 2 && sudo systemctl status watcher.service --no-pager | head -15"

echo "✓ Bootstrap complete — https://${DOMAIN}"
