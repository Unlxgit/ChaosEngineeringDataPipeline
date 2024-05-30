# Chaos Engineering Game Day

## Experiment 1
### execute cleanup script
./src/chaos_experiment/cleanup.ps1

### run experiment1.yaml
kubectl apply -f ./src/chaos_experiment/experiment1.yaml
minikube service api-gateway-service -n gasai --url

run Apache JMeter with port

## Experiment 2
### execute cleanup script
./src/chaos_experiment/cleanup.ps1

### run experiment2.yaml
kubectl apply -f ./src/chaos_experiment/experiment2.yaml
minikube service api-gateway-service -n gasai --url

run Apache JMeter with port

## Experiment 3
### execute cleanup script
./src/chaos_experiment/cleanup.ps1

### run experiment3.yaml
kubectl apply -f ./src/chaos_experiment/experiment3.yaml
minikube service api-gateway-service -n gasai --url

run Apache JMeter with port

## Experiment 4
### execute cleanup script
./src/chaos_experiment/cleanup.ps1

### run experiment4.yaml
kubectl apply -f ./src/chaos_experiment/experiment4.yaml
minikube service api-gateway-service -n gasai --url

run Apache JMeter with port