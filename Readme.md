# Chaos Engineering a Data Pipeline

## Introduction
The system was developed as part of a chaos engineering university course at the University of Agder.
The system is a data pipeline that generates prices and saves them to a database.
Then one forecasting service reads the prices and generates a forecast.
The API Gateway is the entry point for the system and queries the forecast service for the forecast.
The forecast gets saved to the redis cache and can be queried by the API Gateway to reduce the load on the forecast service.

## Resilience Strategies
The system uses the following strategies:
- Retry policies
- Failover mechanisms
- Horizontal scaling
- Health and Readiness checks
- Rolling updates
- Stateless services
- Persistent volumes

## Deployment
The system can be deployed on a Kubernetes cluster.
When the goal is to run the system in a minikube cluster connect.ps1 script can be used to connect to the minikube cluster and set up the environment.
Make sure, that the current kubernetes context is set to the minikube cluster.
By running the buildanddeploy.ps1 script in a Powershell the system will be built and deployed to the kubernetes cluster.
If no link is displayed after running the buildanddeploy.ps1 script, then the last command of the script can be run manually to get the link to the API Gateway.

