FROM python:3.8-alpine
MAINTAINER shivaummethala

# recommended when running python in Docker containers
ENV PYTHONUNBEFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create an user to only run process/app, else root will be default user
RUN adduser -D user
USER user