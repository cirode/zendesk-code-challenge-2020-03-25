from python:3.8.2-alpine

RUN apk add --update \
    python-dev \
    build-base \
    bash \
    libffi-dev \
    openssl-dev \
    && rm  -fr /var/cache/apk/*

WORKDIR /application

RUN pip install poetry

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD bash


