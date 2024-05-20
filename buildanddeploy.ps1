kubectl delete deployment --all
kubectl delete service --all

docker build -t forecast:latest ./src/forecast/
docker build -t api-gateway:latest ./src/gateway/
docker build -t gas-price-pull:latest ./src/gas_price_pull/


kubectl apply -f ./deploy/deployment.yaml

minikube service api-gateway-service -n gasai --url

