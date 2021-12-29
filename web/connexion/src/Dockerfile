FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install flask gunicorn remote_sqlite js2py
COPY ./src /app
WORKDIR /app
CMD gunicorn -b 0.0.0.0:8000 wsgi:app
