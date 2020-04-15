FROM ubuntu:18.04

LABEL maintainer="septnn@163.com"

WORKDIR /home/app

ADD . /home/app/

RUN apt update

RUN apt install -y nginx openssl python3-pip python3-pyaudio sox libatlas-base-dev portaudio19-dev

RUN pip3 install -r /home/app/xiaov/requirements.txt -i https://pypi.douban.com/simple/

EXPOSE 8140-8150

ENTRYPOINT ["/home/app/sh/run.sh"]