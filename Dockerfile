FROM python:3.8-alpine
MAINTAINER shivaummethala

# recommended when running python in Docker containers
ENV PYTHONUNBEFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
# remove all temp dependencies
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create an user to only run process/app, else root will be default user
RUN adduser -D user
USER user

# update - update the registry before we add
# no-cache - do not store the registry index on our docker file to minimize the extra dependencies
# Install some temporary requirement and remove them after the requirements ran
# --virtual - alias to remove all dependecies
# gcc libc-dev linux-headers postgressql-dev - temp dependencies to install postgres alpine