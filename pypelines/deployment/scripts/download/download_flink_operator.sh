#!/bin/bash

FLINK_VERSION="1.8.0"
DOWNLOADS_PATH=deployment/downloads/k8s
LOCAL_FILEPATH=$DOWNLOADS_PATH/flink-operator-$FLINK_VERSION.tgz
DOWNLOAD_URL=https://downloads.apache.org/flink/flink-kubernetes-operator-$FLINK_VERSION/flink-kubernetes-operator-$FLINK_VERSION-helm.tgz


## Download the Flink operator.
mkdir -p $DOWNLOADS_PATH &&
curl -L -o $LOCAL_FILEPATH $DOWNLOAD_URL &&

# Unzip the package
tar -zxvf $LOCAL_FILEPATH -C $DOWNLOADS_PATH
