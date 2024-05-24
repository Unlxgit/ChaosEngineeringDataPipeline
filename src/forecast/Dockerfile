FROM jupyter/scipy-notebook

COPY ../.. /app/
WORKDIR /app

USER root

#RUN apt-get update && \
#    apt-get upgrade -y && \
#    apt-get install -y --no-install-recommends \
#    bash \
#    git \
#    openssh-client && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt --verbose

ENTRYPOINT ["python", "-u", "app.py"]
