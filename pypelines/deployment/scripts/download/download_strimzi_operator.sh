#!/bin/bash

STRIMZI_VERSION="0.39.0"
DOWNLOAD_URL=https://github.com/strimzi/strimzi-kafka-operator/releases/download/$STRIMZI_VERSION/strimzi-cluster-operator-$STRIMZI_VERSION.yaml
DOWNLOADS_PATH=deployment/k8s
LOCAL_FILEPATH=$DOWNLOADS_PATH/strimzi-cluster-operator-$STRIMZI_VERSION.yaml

# Download the Strimzi operator
mkdir -p $DOWNLOADS_PATH &&
curl -p -L -o $LOCAL_FILEPATH $DOWNLOAD_URL &&

# Update the namespace from myproject to default.
sed -i 's/namespace: .*/namespace: default/' $LOCAL_FILEPATH