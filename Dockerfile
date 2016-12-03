#FROM python:2.7.12-alpine
FROM alpine:latest
MAINTAINER shengpf

ENV TECAST_ENV PRODUCT
EXPOSE 4000
VOLUME ["/data/src",]

COPY ./misc /data/base/
COPY ./misc/docker/supervisor.conf /etc/supervisor/conf.d/supervisor_tsbackend.conf
COPY ./misc/pip.conf /etc/pip.conf

RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.4/main" > /etc/apk/repositories

RUN apk add --update \ 
    build-base \
    gcc \
    python \
    python-dev \
    py-pip \
    py-virtualenv \
    py-mysqldb \
    py-pillow \
    supervisor

WORKDIR /data/
RUN virtualenv env
RUN source env/bin/activate
RUN pip install --upgrade pip
RUN pip install -r base/req.txt

CMD ["sh", 'base/docker/gunicorn.sh']
