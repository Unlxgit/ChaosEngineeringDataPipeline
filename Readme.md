
minikube start
minikube docker-env
minikube -p minikube docker-env | Invoke-Expression


minikube tunnel
minikube service list
minikube service prime-consumer-service -n prime --url


kubectl delete deployment --all
kubectl delete service --all

kubectl create namespace gasai
kubectl config set-context --current --namespace=gasai

minikube service prime-consumer-service -n prime --url


kubectl describe deployment prime-deployment -n prime


kubectl get pods -n prime

kubectl describe pod prime-deployment-5584f448fb-2nnjh -n prime

kubectl logs prime-consumer-deployment-66bff547d9-8jztb -n prime