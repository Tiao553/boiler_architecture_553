# <IMG src="https://airflow.apache.org/docs/apache-airflow/1.10.6/_images/pin_large.png" alt="Apache Airflow Documentation — Airflow Documentation" width="30" height="30"  /> Airflow  

Airflow é uma plataforma para criar, agendar e monitorar fluxos de trabalho de maneira programática. Os fluxos de trabalho são criados como Directed Acyclic Graphs (DAGs) de tarefas. O agendador do Airflow executa suas tarefas em uma série de trabalhadores enquanto segue as dependências especificadas. Para este caso, temos dois links que podem ser úteis:

- [Documentação do Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html).
- [Documentação Airflow for Kubernetes](https://airflow.apache.org/docs/helm-chart/stable/index.html).

Conforme é feito para o [SparkOperator](/[BMG]-%2D-Documentação-Engenharia-de-Dados/Infraestrutura/Sparkoperator), o Airflow terá seu próprio namespace no cluster Kubernetes.
```
kubectl create namespace airflow
```

E também é necessário adicionar o repositório do Airflow no Helm. 
```
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

A próxima intrução é um configmap para instalar pacotes dentro dos pods onde será executado o airflow
```
kubectl create -n airflow configmap requirements --from-file=requirements.txt 
```

Agora iremos de fato, instalar o airflow a partir de um template yaml, onde configuramos alguns parâmetros para adequar a imagem as necessidades do ambiente. 
```
helm install -n airflow airflow apache-airflow/airflow -f values_airflow.yaml --debug --timeout 10m0s
```

Precisamos aplicar o patch do comando abaixo para criação de um loadbalancer, que nos permitirá acesso ao airflow via qualquer navegador web.
```
kubectl patch svc airflow-webserver -n airflow  -p '{"spec": {"type": "LoadBalancer"}}'
```

por ultimo basta acessar o aiflow web pelo seu navegador, para [descobrir a url selecione o endereço que aparece no seu load balancer] a porta é a 8080, que você pode descobrir desta maneira:

```
kubectl get svc -n airflow
```

Se todos os passos foram seguidos corretamente, certamente você vai ver a tela de login do airflow quando digitar a url:porta base da sua aplicação no navegador.


Agora precisamos finalizar as ultimas configurações, que estão relacionadas ao uso de dois operadores do airflow: [Spark Kubernetes Operator](https://registry.astronomer.io/providers/kubernetes/modules/sparkkubernetesoperator) e o [Spark Kubernetes Sensor](https://registry.astronomer.io/providers/kubernetes/modules/sparkkubernetessensor), que serão utilizados nas DAGs do airflow para executar as aplicações Spark.  

Devemos criar um conjunto de regras dentro do cluster kubernetes para que o airflow funcione de acordo com o que esperamos, basta executar os comandos abaixo, na ordem em que eles aparecem:

```
kubectl apply -f airflow_rbac.yaml -n processing
```

Realize o login na aplicação web, e no menu superior principal em: 
- Admin > Connections 

Enontre a conexão "kubernetes_default", selecione a opção de editar a conexão, na tela que aparecer com os parâmetros de configuração será necessário marcar apenas um checkbox "In cluster configuration" e salvar a conexão:

Bem, este é o fim das intruções para deploy! :rocket: :rocket:

Vou deixar mais alguns links que me ajudaram durante o deploy do airflow, que podem ser úteis:

- https://marclamberti.com/blog/airflow-on-kubernetes-get-started-in-10-mins/
- https://www.notion.so/Airflow-Helm-Chart-Quick-start-for-Beginners-3e8ee61c8e234a0fb775a07f38a0a8d4
- https://localcoder.org/unable-to-create-sparkapplications-on-kubernetes-cluster-using-sparkkubernetesop