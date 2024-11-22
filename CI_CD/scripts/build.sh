#!/bin/bash

set -e

echo "Building Docker image..."
docker build -t your-docker-repo/taqwanet:latest .
echo "Docker image built successfully."
