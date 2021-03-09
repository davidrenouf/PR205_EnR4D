# Configuration of your master Raspberry pi 4 for Docker utilisation on HypriotOS
# Setting up a Kubernetes 1.11 Raspberry Pi Cluster using kubeadm

In order to set up a Kubernetes 1.11 Raspberry Pi 4 Cluster, there are few steps that you need to follow:
> All the following steps were tested on our Raspberry Pi 4 using external keyboard and screen

## Flashing SD-cards
Start by flashing you SD-card by using etcher that you can get from the following link https://www.balena.io/etcher/ , then you need an operating system either by using the latest version of Raspbian on either raspberrypi.org or directly from https://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-06-29/.
> This process should be done on all the SD-cards. Luckily, we have only one cluster which means ony one SD-card to flash for the Raspberry Pi 4.

### *Flash the SD-card*
Now, insert the SD-card, use the image you just downloaded and then press: `flash`.
When the SD-card is flashed, take it out then put it again on the machine.

### *Enable SSH*
In order to make SSH available on the machine, you need to create a file in the boot directory by using the following comand:
`$ touch /Volumes/boot/ssh`

Unmount the SD-card and put it in the Raspberry Pi. Now you are ready to fire up this little tool!

After that, you should be able to SSH into the Raspberry Pi as follows:
`ssh pi@raspberrypi.local`
`password : raspberry`




