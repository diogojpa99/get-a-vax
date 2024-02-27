FROM python:3.10-slim-bullseye

WORKDIR /app


COPY setup.py ./
COPY getavax/ ./getavax/

RUN pip install -e .

CMD [ "pserve", "./production.ini" ]