FROM alpine:3.6

ADD src/requirements.txt /tmp/requirements.txt

RUN apk add --no-cache --update \
                        bash \
                        gcc \
                        python \
                        py2-pip \
                        postgresql-dev \
                        python-dev \
                        musl-dev \
    && pip install -U pip setuptools \
    && pip install -r /tmp/requirements.txt

ADD src /opt/src

WORKDIR /opt/src

CMD celery -A faas-proxy worker --loglevel=info --concurrency=4