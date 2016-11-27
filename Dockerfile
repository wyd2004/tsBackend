#FROM python:2.7.12-alpine
FROM alpine:latest
MAINTAINER shengpf
ENV TECAST_ENV PRODUCT
EXPOSE 4001


COPY ./src /data/src/
COPY ./misc /data/misc/
COPY ./misc/docker/supervisor.conf /etc/supervisor/conf.d/supervisor_tsbackend.conf
COPY ./misc/pip.conf /etc/pip.conf

RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/v3.5/main" > /etc/apk/repositories
RUN apk add --update \ 
    build-base \
    gcc \
    python \
    python-dev \
    py-pip \
    py-virtualenv \
    #py-gunicorn \
    py-mysqldb \
    py-pillow \
    #py-requests \
    supervisor
WORKDIR /data/
RUN virtualenv env
RUN source env/bin/activate
#RUN pip install -r misc/req.txt
RUN pip install --upgrade pip
RUN pip install -r /data/misc/docker/req.txt
CMD 'misc/docker/gunicorn.sh'
