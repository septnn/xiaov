FROM ubuntu:18.04

LABEL maintainer="septnn@163.com"

WORKDIR /home/app

ADD . /home/app/

RUN apt update

RUN apt install -y nginx openssl python3-pip python3-pyaudio sox libatlas-base-dev portaudio19-dev

RUN rm -f /etc/nginx/nginx.conf && cp /home/app/etc/nginx.conf /etc/nginx/nginx.conf
RUN openssl req -new -newkey rsa:2048 -sha256 -nodes -out /etc/nginx/server.csr -keyout /etc/nginx/server.key -subj "/C=CN/ST=BeiJing/L=BeiJing/O=xiaov Inc./OU=Web Security/CN=192.168.99.100"
RUN openssl x509 -req -days 365 -in /etc/nginx/server.csr -signkey /etc/nginx/server.key -out /etc/nginx/server.crt

RUN pip3 install -r /home/app/xiaov/requirements.txt -i https://pypi.douban.com/simple/

RUN apt remove -y openssl

EXPOSE 8140-8150

# ENTRYPOINT ["/home/app/sh/run.sh"]