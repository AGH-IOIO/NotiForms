#!/bin/bash

IMAGE_NAME=${1:-ioio-backend}

docker build --target dev -t $IMAGE_NAME . && \
    docker run --rm -p 8080:80 $IMAGE_NAME
