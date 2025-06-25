#!/bin/bash

echo "Switching traffic to GREEN version..."
kubectl patch svc myapp-service -p '{"spec":{"selector":{"app":"myapp","version":"green"}}}'
