kubectl delete deployment --all
kubectl delete service --all
docker build -t prime:latest ./src/prediction/
docker build -t connection:latest ./src/connection/
kubectl apply -f ./deploy/deployment.yaml

minikube service prime-consumer-service -n prime --url