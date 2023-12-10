#!/bin/bash

# Build the Docker image
docker buildx build --platform linux/amd64 -t Eagle_project_full .

# Tag the Docker image
docker tag Eagle_project_full us-central1-docker.pkg.dev/sandbox/Eagle-repo/Eagle_project_full
# Push the Docker image

docker push  us-central1-docker.pkg.dev/sandbox/Eagle-repo/Eagle_project_full


