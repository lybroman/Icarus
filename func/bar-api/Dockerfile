FROM alpine:3.6

RUN apk update && apk add --no-cache --update \
              bash \
              curl \
              python \
              python-dev \
              py2-pip \
              gzip \
              cloc \
  && pip install --upgrade pip \
  && rm /var/cache/apk/*

RUN echo "Pulling watchdog binary from Github." \
    && curl -vsSL https://github.com/openfaas/faas/releases/download/0.8.0/fwatchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog

WORKDIR /root/

COPY index.py           .
COPY requirements.txt   .
RUN pip install -r requirements.txt

COPY function           function

RUN touch ./function/__init__.py

WORKDIR /root/function/
COPY function/requirements.txt	.
RUN pip install -r requirements.txt

WORKDIR /root/

ENV fprocess="python index.py"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
