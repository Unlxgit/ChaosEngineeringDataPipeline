
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

minikube service api-gateway-service -n gasai --url


kubectl describe deployment prime-deployment -n prime


kubectl get pods -n gasai

kubectl describe pod gas-price-pull-deployment-dddb88475-7mvwg -n gasai

kubectl logs gas-price-pull-deployment-dddb88475-7mvwg -n gasai