#!/bin/bash

BEAM_VERSION="2.56.0"
REPO_BASE_URL=https://repo1.maven.org/maven2/org/apache/beam
DOWNLOAD_URL=$REPO_BASE_URL/beam-sdks-java-io-expansion-service/$BEAM_VERSION/beam-sdks-java-io-expansion-service-$BEAM_VERSION.jar
DOWNLOADS_PATH=deployment/downloads/jar
LOCAL_FILEPATH=$DOWNLOADS_PATH/beam-sdks-java-io-expansion-service.jar

# Down
mkdir -p $DOWNLOADS_PATH &&
curl -L -o $LOCAL_FILEPATH $DOWNLOAD_URL