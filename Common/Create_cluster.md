# How to re create a k8s cluster with kubeadm on Raspebrry pi

Once kubeadm is installed and weel configure, you will have to re create the k8s cluster each time you re start the Raspberry pi. In order to automate this part, bash scripts were created.
Commands to connect to Raspberry :
- Master
``
ssh pi@k8s-master.local
``
- Worker
``
ssh pi@k8s-worker-02.local
``

## Bash script on the master

When you connect to the master with ssh, the script starts. You only have to answer "y" when the system ask your permission to continue the process.
Once the process is done, kubeadm is initialized on the master and ready to accept worker nodes.

## On the worker

First, you have to reset the last kubeadm configuration. To do so, you have to disable the swap on the Raspberry pi. Go to the "Desktop" directory and use the next command :
``
sh disable_swap.sh
``
Once the swap is disabled, use the commad line:
``
sudo kubeadm reset
``
Then, your Raspberry pi is ready to join the k8s cluster.

## Get the kubeadm join command on the master

Go to the home directory on the master and use the next command :
``
cat token
``
This command will print you the content of the file token. Then copy the two last lines which begin with "kubeadm join". The command contains the token you need to connect the worker node to the master node.

## Use the copied line on the worker node
Go to the worker node and use the command line you had copied. This command must connect you to the k8s cluster!

## Add a container network
Don't forget to add the container network with the next command line on the master node :
``
sudo kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
``



