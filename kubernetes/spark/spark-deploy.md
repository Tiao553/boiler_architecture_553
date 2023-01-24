# Sparkoperator


O Kubernetes Operator para Apache Spark visa tornar a especificação e execução de aplicativos Spark tão fácil quanto a execução de outras aplicações no Kubernetes. Ele usa recursos personalizados do Kubernetes para especificar, executar e exibir o status de aplicativos Spark. Se caso quiser saber mais sobre o SparkOperator, clique [aqui](https://googlecloudplatform.github.io/spark-on-k8s-operator/) e seja redirecionado para a documentação oficial. Agora, vamos as intruções. Por padrão definimos o nome da nossa namespace como processing, lá deverá ser executadas todas as aplicações spark.



1 . Crie o namespace onde os seus recursos serão instaciados
```
kubectl create namespace processing
```
2 . Adicione o repositório do helm que contém a imagem do SparkOperator  
```
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm repo update
helm install --set image.tag=v1beta2-1.3.2-3.1.1 spark spark-operator/spark-operator --namespace processing --create-namespace
helm ls -n processing
```

3 . Agora iremos criar uma conta de serviço e uma role, no namespace.
```
kubectl create serviceaccount spark -n processing
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=processing:spark --namespace=processing
```

4 . E finalmente para executar a nossa aplicação Spark, aplicamos o devido template e indicamos o namespace.
```
kubectl apply -f caminho_do_arquivo/arquivo.yml -n processing
```
<br>

### :crystal_ball: Comandos utéis

- #### Logs 
Os comando abaixo são apenas pra acompanhamento doss logs de configuração do SparkOperator e logs de execução da aplicação Spark respectivamente.
```
kubectl get sparkapplication <sua spark aplication>  -n processing -oyaml
kubectl logs -f <driver da sua spark aplication> -n processing
```

- ####Criação de secret

Caso precise criar um secret dentro do Kubernetes siga as instruções a seguir. Nesse exemplo iremos passar as credencias do usuário AWS que deverá ler os dados via SparkOperator. Neste caso basta apenas copiar o trecho abaixo e inserir as credencias no local indicado. Se quiser entender como funciona os secrets no Kubernetes, basta acessar esta [documentação](https://kubernetes.io/docs/concepts/configuration/secret/).
```
kubectl create secret generic aws-credentials --from-literal=aws_access_key_id=<put_your_key_here> --from-literal=aws_secret_access_key=<puy_your_secret_here> -n processing
```

- #### Deletar Aplicações Spark no Kubernetes
Ao trabalhar com Spark no Kubernetes, para deletar alguma aplicação, não se recomenda remover o pod diretamente. O método sugerido para tal operação é _delete sparkapplication_.
Para tal, é necessário obter o nome da aplicação. Há duas formas de se obter essa informação:
```
kubectl get sparkapplications -n <namespace>
```
Ou copiar o conteúdo antes de "-driver" do nome do pod, conforme exemplo da figura abaixo.
Para deletar a spark application:
```
kubectl delete sparkapplication <sparkapp> -n <namespace>
```


