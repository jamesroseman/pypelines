#!/bin/bash

eval $(minikube docker-env) &&
docker build -t pypelines-beam:1.16 -f ./pypelines/deployment/docker/Dockerfile.beam ./pypelines/deployment/ &&
docker build -t pypelines-beam-harness:2.56.0 -f ./pypelines/deployment/docker/Dockerfile.beam-harness ./pypelines/deployment/