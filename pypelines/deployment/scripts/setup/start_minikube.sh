#!/bin/bash

minikube start --cpus='max' --memory=20480 \
  --addons=metrics-server --kubernetes-version=v1.25.3