FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk upgrade && apk add --no-cache bash git openssh
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]