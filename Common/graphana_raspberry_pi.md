# Setting up Grafana on the Raspberry Pi

In this document, we will be walking you through all the steps of installing and setting up Grafana on the Raspbian operating system.

### Equipement
- Raspberry Pi
- Micro SD Card
- Ethernet cord or Wifi Dongle
- USB Keyboard
- Mouse
- HDMI Cable
> The last three equipements can be optional.

## Installing Graphana to the Raspberry Pi

Before installing Graphana, you need to make sure that all the packages are up to date.
- <code> sudo apt update </code>
- <code> sudo apt upgrade </code>

Then, you can add the Graphana package repository:
- <code> wget -q -O - https://packages.grafana.com/gpg.key | sudo  apt-key add - </code>
- <code> echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list </Code>

Once you made changes to your package list, you need to run an update.
- <code> sudo apt update </code>

You can now install the latest version of Grafana by running the following command on your device.
- <code> sudo apt install grafana </code>

To start the startup, you can enable Grafana to start at boot, all you need to do is run the following command.
- <code> sudo systemctl enable grafana-server </code>

Now, let’s start up the Grafana server software by running the command below in the Pi’s terminal.
- <code> sudo systemctl start grafana-server </code>

## Connecting Grafana Installation to the Raspberry Pi

First, retrieve the local IP address of your Raspberry Pi. you can use this IP to access Grafana remotely within your local network. To do so, use the following command:
- <code> hostname -I </code>

Grafana’s web interface sits on port 3000 of your Raspberry Pi’s IP address.
Make sure that you replace “<IPADDRESS>” with the IP that you retrieved in the previous step.
- <code> http://<IPADDRESS>:3000 </code>

Now, you are able to see the Grafana login screen loading up.

On this screen, you will be able to login using the default admin user that was created when you first installed Grafana to your Raspberry Pi.

- Username : admin
- Password : admin

Then you will be asked to change the password, change it then press save.

Once you have logged in and changed the default password, you should now be greeted with the Grafana main screen.

Congrats! You have now Grafana up and running on your Raspberry Pi and you are able to access its web interface.
