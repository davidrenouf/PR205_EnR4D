# Basic commands to control pod deployments

In order to orchestrate the deployments on your cluster, you can use Kubernetes basic tools. 
## Node Label
With the Node Selector parameter, you can specify a label for a node. In this example, we will lebellize our node with disktype=ssd. This label signifies that the node disktype is an ssd. In consequence, you can deploy pods which need to be run on ssd disk on this node.
To do so, add this label with the following command :
```shell
kubectl label nodes <your-node-name> disktype=ssd
```
Then, you have to create a pod config file (named node_selector.yaml for example) and to specify a node selector :
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx_with_node_selector
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disktype: ssd
```
To deploy your pod :
```shell
kubectl apply -f node_selector.yaml
```
You can verify that your pod is deployed on the right node with the following command :
```shell
kubectl get pods -o wide
```
## Node Affinity
Node Affinity parameter is an 'extension' of Node Label. It does the same thing but you can specify more conditions. Let's try to deploy a pod on a node labelled green=yes. 

As before, you have to labelize your node :
```shell
kubectl label nodes <your-node-name> green=yes
```
Then, you have to create a pod config file (named node_affinity.yaml for example) and to specify a node affinity :
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: "green"
            operator: In
            values: ["yes"]
         
  containers:
  - name: with-node-affinity
    image: nginx
```
The config file specify that the pod can only be scheduled on a node with the label green=yes. 

From k8s documentation :
There are currently two types of node affinity, called `requiredDuringSchedulingIgnoredDuringExecution` and `preferredDuringSchedulingIgnoredDuringExecution`. You can think of them as "hard" and "soft" respectively, in the sense that the former specifies rules that _must_ be met for a pod to be scheduled onto a node (just like `nodeSelector` but using a more expressive syntax), while the latter specifies _preferences_ that the scheduler will try to enforce but will not guarantee.

To deploy your pod :
```shell
kubectl apply -f node_affinity.yaml
```
You can verify that your pod is deployed on the right node with the following command :
```shell
kubectl get pods -o wide
```

## Taints & Tolerations
Node affinity, is a property of  Pods that  _attracts_  them to a set of  nodes (either as a preference or a hard requirement).  _Taints_  are the opposite -- they allow a node to repel a set of pods.

_Tolerations_  are applied to pods, and allow (but do not require) the pods to schedule onto nodes with matching taints.

Taints and tolerations work together to ensure that pods are not scheduled onto inappropriate nodes. One or more taints are applied to a node; this marks that the node should not accept any pods that do not tolerate the taints.

Let's taint a node and add a toleration on a pod :
```shell
kubectl taint nodes <your-node-name> key1=value1:NoSchedule
```
The NoSchedule parameter means that pods couldn't be deployed on this node without the good toleration.
To see if your node is indeed taint, use the following command :
```shell
kubectl describe node
```
You should see a parameter 'Taints' on you tainted node with the value key1=value1:NoSchedule.

Now, let's add a toleration to a pod - create a pod config file (named node_tainted.yaml for example) and specify a parameter "tolerations" :
```yaml
apiVersion: v1  
kind: Pod  
metadata:  
  name: with-taints-tolerations  
  labels:  
    env: test  
spec:  
  containers:  
  - name: with-taints-tolerations  
    image: nginx  
    imagePullPolicy: IfNotPresent  
  tolerations:  
  - key: "key1"  
    operator: "Exists"  
    effect: "NoSchedule"
```
A toleration "matches" a taint if the keys are the same and the effects are the same, and:

-   the  `operator`  is  `Exists`  (in which case no  `value`  should be specified), or
-   the  `operator`  is  `Equal`  and the  `value` are equal.
- 
The above example used `effect` of `NoSchedule`. Alternatively, you can use `effect` of `PreferNoSchedule`. This is a "preference" or "soft" version of `NoSchedule` -- the system will _try_ to avoid placing a pod that does not tolerate the taint on the node, but it is not required.

To deploy your pod :
```shell
kubectl apply -f node_tainted.yaml
```
You can verify where your pod is deployed with the following command :
```shell
kubectl get pods -o wide
```
