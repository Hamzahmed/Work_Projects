#!/bin/bash

# Build the Docker image
docker buildx build --platform linux/amd64 -t Eagle_revperiod_full .

# Tag the Docker image
docker tag Eagle_revperiod_full us-central1-docker.pkg.dev/sandbox/Eagle-repo/Eagle_revperiod_full

# Push the Docker image
docker push us-central1-docker.pkg.dev/sandbox/Eagle-repo/Eagle_revperiod_full