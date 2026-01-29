#!/bin/bash
DOMAIN="welcome-to-the-wedding.ru"
EMAIL="simonchuka96@gmail.com"

mkdir -p nginx/ssl

docker run --rm \
  -v $(pwd)/certbot-conf:/etc/letsencrypt \
  -v $(pwd)/certbot-webroot:/var/www/certbot \
  certbot/certbot:latest \
  certonly --webroot --webroot-path=/var/www/certbot \
  --email $EMAIL --agree-tos --no-eff-email \
  -d $DOMAIN -d www.$DOMAIN

ln -sf $(pwd)/certbot-conf/live/$DOMAIN/fullchain.pem nginx/ssl/fullchain.pem
ln -sf $(pwd)/certbot-conf/live/$DOMAIN/privkey.pem nginx/ssl/privkey.pem

echo "SSL установлен! Перезапустите nginx: docker-compose restart nginx-proxy"
