FROM --platform=linux/amd64 bitnami/python:3.9-debian-11

# Set the working directory in the container
WORKDIR /app
EXPOSE 8080
ENV PORT 8080

ENV HOST 0.0.0.0

# Load environment variables from .env file
ENV $(cat .env | grep -v ^# | xargs)

# Set the working directory to /app/ETL_Service
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
COPY install_postgres.sh /app/
RUN ./install_postgres.sh

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY entry_point.sh /app/

RUN ./entry_point.sh

# Copy the rest of the application code into the container at /app

COPY . /app/

RUN curl -o /app/geojson-counties-fips.json https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json
RUN curl -o /app/ccc_compiled_2021-present.csv https://raw.githubusercontent.com/nonviolent-action-lab/crowd-counting-consortium/master/ccc_compiled_2021-present.csv

# Define the command to run your application
ENTRYPOINT ["python3", "ETL_Service.py"]
