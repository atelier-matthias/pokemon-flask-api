FROM python:3

ENV ROOT /srv/pokemon-api-flask

RUN mkdir $ROOT

WORKDIR $ROOT
EXPOSE 8989

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .
