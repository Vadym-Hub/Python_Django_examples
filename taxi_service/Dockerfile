# syntax=docker/dockerfile:1
#Tells Docker to use the official python 3 image from dockerhub as a base image
FROM python:3

# Sets an environmental variable that ensures output from python is sent straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

# Sets the container's working directory to /app
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /code/