#FROM python:2.7.12-alpine
FROM alpine:latest
MAINTAINER shengpf

EXPOSE 4000


COPY ./misc /data/misc/
COPY ./misc/docker/supervisor.conf /etc/supervisor.d/tsbackend.ini
COPY ./misc/pip.conf /etc/pip.conf

RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.4/main" > /etc/apk/repositories && \
apk add --update \ 
    build-base \
    gcc \
    python \
    python-dev \
    py-pip \
#    py-virtualenv \
    supervisor \ 
    zlib-dev \
    libjpeg-turbo-dev  && \
cd /data/ && \
#virtualenv env && \
apk add --update py-mysqldb && \
#source env/bin/activate && \
pip install --upgrade pip && \
pip install -r misc/docker/req.txt 

WORKDIR /data/

CMD ["supervisord", "-nc", "/etc/supervisord.conf"]
