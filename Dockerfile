FROM python:alpine3.6

RUN set -ex \
    && apk add --update cmake ca-certificates bash make g++ \
    && update-ca-certificates \
    && apk add openssl \

    && wget "https://github.com/google/brotli/archive/v1.0.1.tar.gz" -O /tmp/brotli.tar.gz \
    && tar xf /tmp/brotli.tar.gz -C /tmp \
    && cd /tmp/brotli-1.0.1 \
    && ./configure-cmake \
    && make install \
    && cd /tmp && rm -rf /tmp/brotli* \

    && wget https://downloads.sourceforge.net/project/optipng/OptiPNG/optipng-0.7.6/optipng-0.7.6.tar.gz -O /tmp/optipng.tar.gz \
    && tar xf /tmp/optipng.tar.gz -C /tmp \
    && cd /tmp/optipng-0.7.6 \
    && ./configure \
    && make install \
    && rm -rf /tmp/optipng* \

    && apk del openssl cmake ca-certificates bash make g++

ADD . /data/app

WORKDIR "/work"

ENTRYPOINT ["python", "/data/app/compress.py"]
