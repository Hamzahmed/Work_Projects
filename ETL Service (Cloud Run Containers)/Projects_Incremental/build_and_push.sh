#!/bin/bash

# Build the Docker image
docker buildx build --platform linux/amd64 -t Eagle_project_incremental .

# Tag the Docker image
docker tag Eagle_project_incremental us-central1-docker.pkg.dev/sandbox/Eagle-repo/Eagle_project_incremental_load

# Push the Docker image
docker push us-central1-docker.pkg.dev/sandbox/Eagle-repo/Eagle_project_incremental_load