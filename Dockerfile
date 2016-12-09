#FROM python:2.7.12-alpine
#FROM alpine:latest
FROM django
MAINTAINER shengpf

ENV TECAST_ENV PRODUCT
EXPOSE 4000
#VOLUME ["/data/src",]

COPY ./misc /data/misc/
COPY ./misc/docker/supervisor.conf /etc/supervisor.d/tsbackend.ini
COPY ./misc/pip.conf /etc/pip.conf

RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.4/main" > /etc/apk/repositories

RUN apk add --update \ 
    build-base \
    gcc \
    python \
    python-dev \
    py-pip \
    py-virtualenv \
    supervisor \ 
    zlib-dev \
    libjpeg-turbo-dev 

WORKDIR /data/
RUN virtualenv env
RUN source env/bin/activate
RUN pip install --upgrade pip
RUN pip install -r misc/docker/req.txt
RUN mkdir -p /var/log/supervisor/

CMD ["supervisord", "-nc", "/etc/supervisord.conf"]
