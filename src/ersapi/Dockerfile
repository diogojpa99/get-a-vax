FROM python:3.10-slim-bullseye

WORKDIR /app


COPY ./app.py /app

RUN pip install flask

CMD flask run -h 0.0.0.0
