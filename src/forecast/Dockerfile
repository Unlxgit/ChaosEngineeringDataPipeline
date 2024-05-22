FROM python:3.10-alpine

COPY ../.. /app/
WORKDIR /app

RUN apk update && apk upgrade && apk add --no-cache \
    bash \
    git \
    openssh \
    build-base \
    postgresql-dev \
    gcc \
    libc-dev \
    musl-dev \
    linux-headers

RUN pip3 install -r requirements.txt --verbose

ENTRYPOINT ["python", "-u", "app.py"]
