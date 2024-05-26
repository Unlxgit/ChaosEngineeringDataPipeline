kubectl delete deployment --all
kubectl delete service --all
# kubectl delete pvc --all
# kubectl delete pv --all

docker build -t forecast:latest ./src/forecast/
docker build -t api-gateway:latest ./src/api_gateway/
docker build -t price-generation:latest ./src/price_generation/


kubectl apply -f ./deploy/deployment.yaml

minikube service api-gateway-service -n gasai --url