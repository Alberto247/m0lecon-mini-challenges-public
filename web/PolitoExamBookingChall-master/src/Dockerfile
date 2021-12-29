FROM python:3.9
RUN apt-get update
COPY ./app /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn
ENTRYPOINT ["gunicorn", "-w", "4", "--bind", ":5000", "app:app"]
