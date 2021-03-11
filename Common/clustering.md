# Building a cluster using Raspberry Pi and Kubernetes

After configuring you Raspberry Pi 3 and 4, you need now to build a cluster using Kubernetes in order to schedule images of a given architecture and run them on the appropriate nodes by Kubernetes' scheduler through the use of Kubernetes taints and tolerations.

## Requirements
This process will require the few following elements:
- 1 Raspberry Pi 4 that will be the master or the control plane of your nodes
- 3 Raspberry Pi 3 that will be the slaves or the computing nodes

## Building the cluster
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
