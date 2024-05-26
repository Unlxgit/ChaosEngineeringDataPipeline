minikube start
minikube docker-env
minikube -p minikube docker-env | Invoke-Expression

#kubectl delete namespace gasai
#kubectl create namespace gasai
kubectl config set-context --current --namespace=gasai
