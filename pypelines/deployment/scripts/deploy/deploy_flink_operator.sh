#!/bin/bash

DOWNLOADS_PATH=deployment/downloads/k8s

# Uninstall the Flink operator, if it exists.
if helm list | grep -q "^flink-kubernetes-operator"; then
  helm uninstall flink-kubernetes-operator
fi

# Install the Flink operator
helm install flink-kubernetes-operator ./$DOWNLOADS_PATH/flink-kubernetes-operator