# Configuration of your slave Raspberry pi 3 for Docker utilisation on HypriotOS
# HypriotOS installation 

To install **HypriotOS**, the OS adapted to **docker**, you have to first download it on https://blog.hypriot.com/downloads/, the site with the documentation associated. Then you have to flash it on your SD card, you can use *belenaEtcher* to higher simplicity. 
You put then the SD card in the Raspberry pi 3 and turn it on .
> Note that you need an external screen and keyboard plugged to your Raspberry for the initialisation.

At this point, the OS is automatically installed and ready to be used.  You just have to log in on with :
Login : pirate
Password : hypriot

# SSH activation
In order to activate *ssh* you have to follow these steps : 

- Use the command bash : <code> sudo raspi-config </code> 
- Select *5. Interfacing Options* 
- Select *P2 SSH* 
- Select yes for "Enable SSH" 

Congratulation, you have your ssh activated ! 

To connect to the Raspberry, use the command :
<code> ssh pirate@black-pearl.local </code> 
with the password : hypriot. 


## Wifi configuration and activation

The wifi is not configurated by default, so you must activate it in order to connect to the Raspberry in ssh. 
Use the command : 
<code> sudo nano /etc/wpa_supplicant/wpa_supplicant.conf </code> 
Modify the file by writing :
<code> network={ 
ssid="Your box SSID"
psk="Your box password"
proto=RSN
key_mgmt=WPA-PSK
pairwise=CCMP
auth_alg=OPEN
}
</code>
Then you have to reboot the Rasberry and the Wifi is activated !


## Run Docker

- Before starting, you have to have your system uptaded :
<code>   sudo apt-get update && sudo apt-get upgrade </code>
- Then dowload the installation file :
<code>   curl -fsSL https://get.docker.com -o get-docker.sh <code>
- Run the script :
<code> sudo sh get-docker.sh </code> 
- Give rights access for the user :
<code> sudo usermod -aG docker pi </code> 
- Run the hello world container :
<code> docker run hello-world </code> 

## Bonus : switch your keyboard to azerty 

Here there are few steps to switch the keyboard linked to the Raspberry to azerty temporarely :
- Install the correct thing :
<code> sudot apt install console-data </code> 
- Reconfigure the keyboard :
<code> sudo dpkg-reconfigure console-data </code>
- Select "Select keymap from full list"
- Select "pc / azerty / French / Same as X11 (latin9) / Standard"

There you go ! 
> Becarefull, if you reboot the Raspberry, you will have to do this thing once again. 


