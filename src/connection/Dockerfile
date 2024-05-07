FROM python:3.12-alpine

COPY ../.. /app/
WORKDIR /app

RUN apk update && apk upgrade && apk add --no-cache bash git openssh
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "-u", "app.py"]
