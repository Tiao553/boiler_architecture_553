Para adicionar o cluter EKS no kubeconfig 

```sh
aws eks -region us-east-1  update-kubeconfig --name a3-k8s-stack-spark-3-2
```

Verificar se esta no cluster certo o kubectl 
```sh
kubectl config get-contexts
```

Instalar as aplicações geração de metricas dos cluster 
```sh
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/high-availability.yaml
# espera um minutinho gerar o serviço
kubectl top nodes
```

Instalar ferramentas de facilitação de acesso a namespaces e cluster
```sh
sudo apt-get update
sudo git clone https://github.com/ahmetb/kubectx /usr/local/kubectx
sudo ln -s /usr/local/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /usr/local/kubectx/kubens /usr/local/bin/kubens
```