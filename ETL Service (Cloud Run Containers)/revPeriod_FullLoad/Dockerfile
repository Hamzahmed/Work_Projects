#!/bin/python3

FROM --platform=linux/amd64 bitnami/python:3.9-debian-11

# Set the working directory in the container
WORKDIR /app

EXPOSE 8080
ENV PORT 8080

ENV HOST 0.0.0.0


ENV GCC_VERSION=9.3.0

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

# Update the package repository and install required packages
RUN apt-get update && \
    apt-get install -y \
    python3.9 \
    python3-pip \
    curl \
    apt-transport-https \
    gnupg

# Install any other system dependencies you need
COPY install_odbc.sh /app/
RUN ./install_odbc.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev \
    python3.9-dev


# Install the Google Cloud SDK
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && apt-get install -y google-cloud-sdk

# Set an environment variable to point to the copied credentials file
ENV GOOGLE_APPLICATION_CREDENTIALS /app/gcp-connection.json


# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/

RUN ./entrypoint.sh

COPY run_isql.sh /app/

RUN ./run_isql.sh


# Copy the rest of the application code into the container at /app
COPY . /app/



# Define the command to run your application

ENTRYPOINT ["python3","main.py"]

