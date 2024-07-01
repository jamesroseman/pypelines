#!/bin/bash

DOWNLOAD_URL=https://github.com/jetstack/cert-manager/releases/download/v1.8.2/cert-manager.yaml
DOWNLOAD_PATH=pypelines/deployment/downloads/k8s/cert-manager.yaml

curl -L -o $DOWNLOAD_PATH $DOWNLOAD_URL
