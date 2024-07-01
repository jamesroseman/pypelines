#!/bin/bash

STRIMZI_VERSION="0.39.0"

# Deploy Strimzi operator
kubectl apply -f deployment/k8s/strimzi-cluster-operator-$STRIMZI_VERSION.yaml &&

# Verify Strimzi operator
kubectl get deploy,rs,po &&

# Deploy Kafka Cluster
kubectl apply -f deployment/k8s/kafka-cluster.yaml &&

# Deploy Kafka UI
kubectl apply -f deployment/k8s/kafka-ui.yaml &&

# Verify Kafka Cluster deployment
kubectl get po,strimzipodsets.core.strimzi.io,svc -l app.kubernetes.io/instance=demo-cluster &&

# Verify Kafka UI deployment
kubectl get all -l app=kafka-ui &&

# Forward Kafka port
kubectl port-forward svc/demo-cluster-kafka-external-bootstrap 29092 &

# Forward Kafka UI port
kubectl port-forward svc/kafka-ui 8080