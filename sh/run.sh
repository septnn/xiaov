#!/bin/sh

rm -f /etc/nginx/nginx.conf && cp /home/app/etc/nginx.conf /etc/nginx/nginx.conf

openssl req -new -newkey rsa:2048 -sha256 -nodes -out /etc/nginx/server.csr -keyout /etc/nginx/server.key -subj "/C=CN/ST=BeiJing/L=BeiJing/O=xiaov Inc./OU=Web Security/CN=192.168.99.100"
openssl x509 -req -days 365 -in /etc/nginx/server.csr -signkey /etc/nginx/server.key -out /etc/nginx/server.crt

apt remove -y openssl

nginx && cd /home/app/xiaov && python3 /home/app/xiaov/websocket.py