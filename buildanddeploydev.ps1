docker build -t gas-price-pull:latest ./src/gas_price_pull/

kubectl apply -f ./deploy/deployment_temp.yaml
