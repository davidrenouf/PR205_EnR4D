# Building a cluster using Raspberry Pi and Kubernetes

After configuring you Raspberry Pi 3 and 4, you need now to build a cluster using Kubernetes in order to schedule images of a given architecture and run them on the appropriate nodes by Kubernetes' scheduler through the use of Kubernetes taints and tolerations.

## Requirements
This process will require the few following elements:
- 1 Raspberry Pi 4 that will be the master or the control plane of your nodes
- 3 Raspberry Pi 3 that will be the slaves or the computing nodes

## Initializing each Raspberry Pi
After configuring all your material which means the 4 Raspberry Pi's, you should run your program `hostname_and_ip.sh` in all the previous elements, to do so, you will need:
- the new hostname of each Raspberry Pi
- the new static IP of each Raspberry Pi
- the IP of your Router

Then use the following commands:
#### *Master :* 
`$ sh hostname_and_ip.sh k8s-master 192.168.1.100 192.168.1.1`
#### *Slave 1 :*
`$ sh hostname_and_ip.sh k8s-worker-01 192.168.1.101 192.168.1.1`
#### *Slave 2 :*
`$ sh hostname_and_ip.sh k8s-worker-02 192.168.1.102 192.168.1.1`
#### *Slave 3:*
`$ sh hostname_and_ip.sh k8s-worker-03 192.168.1.103 192.168.1.1`

Now REBOOT you Rasberry Pis, you shoud have the access to all of them via SSH using the following commands:
#### *Master :* 
`ssh pi@k8s-master.local`
#### *Slave 1 :*
`ssh pi@k8s-worker-01.local`
#### *Slave 2 :*
`ssh pi@k8s-worker-02.local`
#### *Slave 3:*
`ssh pi@k8s-worker-03.local`

## Building the cluster with kubeadm
In order to create the k8s cluster, we will use `kubeadm`. It allows you to set up a cluster that will pass the Kubernetes Conformance tests.

### Master node configuration
First, we have to install `kubeadm` on the master node. To do so, you have to run the following program :
  ```sh
  #!/bin/sh
  #Install Docker
  curl -sSL get.docker.com | sh && \
  sudo usermod pi -aG docker

  #Disable Swap
  sudo dphys-swapfile swapoff && \
  sudo dphys-swapfile uninstall && \
  sudo update-rc.d dphys-swapfile remove
  echo Adding " cgroup_enable=cpuset cgroup_enable=memory" to /boot/cmdline.txt
  sudo cp /boot/cmdline.txt /boot/cmdline_backup.txt
  orig="$(head -n1 /boot/cmdline.txt) cgroup_enable=cpuset cgroup_enable=memory"
  echo $orig | sudo tee /boot/cmdline.txt

  #Add repo list and install kubeadm
  curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - && \
  echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list && \
  sudo apt-get update -q && \
  sudo apt-get install -qy kubeadm
```
This program downloads Docker on your device, disables swap and installs `kubeadm`.
Then, you have to initialize kubeadm by running this command :

    $ kubeadm init
Once the process is finish, you shoud have this output :
![PR205_EnR4D](img/clusterinit.png)

The last 2 lines give you the command to join the cluster. We will use it later.
Then, you have to follow the instructions given in the output :

    $ mkdir -p $HOME/.kube
    $ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    $ sudo chown $(id -u):$(id -g) $HOME/.kube/config

Finally, your node master is set up. You can verify its status with the next command line :
    
    $ kubectl get nodes
    
You must see this output :
![PR205_EnR4D](img/clusterinit.png)


### Worker node configuration
As the master node configuration, you have to install `kubeadm`. You can refer to the previous part. Once `kubeadm` is installed, you have to join the cluster created before. You have to run the next command line given in the last part :

    $ sudo kubeadm join --token TOKEN 192.168.1.100:6443 --discovery-token-ca-cert-hash HASH

You have to repeat this process for every Raspberry.
Here an example of what you should see after joining the cluster :
-insert img

### Add a container network

As you can see in this picture, the core-dns pods aren't running. They are in a pending state.
![PR205_EnR4D](img/issue.png)

Nodes are not able to communicate without a container network, which is something you have to provide. Therefore, the final piece of the puzzle is to add one. We will be using weave-net for this. On the master node, run the following command:

    $ kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

With the container network added, you can verify the good health of the cluster :
![PR205_EnR4D](img/fixproblem.png)



## Test your cluster

In order to test the cluster, you can deploy a pod :
![PR205_EnR4D](img/exemple.png)
![PR205_EnR4D](img/ex2.png)


