
```sh
kubectl create namespace cicd
```

# add & update helm list repos
```
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```

# install crd's [custom resources]


> argo-cd ->  https://artifacthub.io/packages/helm/argo/argo-cd
> https://github.com/argoproj/argo-helm

```sh
helm install argocd argo/argo-cd --namespace cicd --version 3.26.8
```
# install argo-cd [gitops]
> create service type load balance on load balancer
```sh
kubectl patch svc argocd-server -n cicd -p '{"spec": {"type": "LoadBalancer"}}'
```

# retrieve load balancer ip
> Check cluster-ip create on kubernetes to loadbalance argo
```sh
kubectl get svc -n cicd
```

> Outra forma de coletar caso existam mais de um é consultado no etcd e em um cluter kubernetes

```sh
kubens cicd && kubectl get services -l app.kubernetes.io/name=argocd-server,app.kubernetes.io/instance=argocd -o jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"
```

# get password to log into argocd portal
```sh
# argocd login IP --username admin --password senha --insecure
# argocd login 10.107.11.62 --username admin --password a6j-fodHKEUmnQk9 --insecure
ARGOCD_LB="ip que estiver no loadbalance"
kubectl get secret/argocd-initial-admin-secret -n cicd -o jsonpath="{.data.password}" | base64 -d | xargs -t -I {} argocd login $ARGOCD_LB --username admin --password {} --insecure
```

# create cluster role binding for admin user [sa]
```sh
kubectl create clusterrolebinding cluster-admin-binding --clusterrole=cluster-admin --user=system:serviceaccount:cicd:argocd-application-controller -n cicd
```

# register cluster
```sh
CLUSTER="cluster-name"
argocd cluster add $CLUSTER --in-cluster
```

# add repo into argo-cd repositories
```sh
REPOSITORY="https://bitbucket.org/git"
argocd repo add $REPOSITORY --username [NAME] --password [PWD] --port-forward
```