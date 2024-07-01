#!/bin/bash

eval $(minikube docker-env) &&
docker build -t beam-python-example:1.16 -f ./deployment/docker/Dockerfile.beam ./deployment/docker/ &&
docker build -t beam-python-harness:2.56.0 -f ./deployment/docker/Dockerfile.beam-harness ./deployment/docker/