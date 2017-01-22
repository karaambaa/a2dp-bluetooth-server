# a2dp-bluetooth-server

The Bluetooth-part was taken from [oleq](https://gist.github.com/oleq/24e09112b07464acbda1 "A2DP audio streaming using Raspberry PI (Raspbian Jessie)")

The Bluetooth profile which does the magic is called [A2DP](https://en.wikipedia.org/wiki/List_of_Bluetooth_profiles#Advanced_Audio_Distribution_Profile_.28A2DP.29).

## Obtaining peripherals

```
pi@raspberrypi:~ $ lsusb
...
Bus 001 Device 008: ID 041e:30d3 Creative Technology, Ltd Sound Blaster Play!
...
Bus 001 Device 012: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode)
...
```

### Audio interface

The on–board audio produces low–quality, noisy output, so I decided to use something better. I chose external USB **Creative Sound Blaster Play!** interface. It costs ~$20.

### Bluetooth dongle

As for Bluetooth dongle, I used **Digitus Tiny USB-Adapter**, which is discovered as `Cambridge Silicon Radio, Ltd Bluetooth Dongle`.

**Note**: I used another dongle (different manufacturer) also discovered as `Cambridge Silicon Radio` but unable to stream audio. So beware, because different manufacturers use the same hardware in a different way. Or they pretend to use the same hardware for some (compatibility?) reasons. This way or another, if you get garbled audio or no audio at all but everything else is alright, don't worry, just try another dongle – it's cheap.

See [RPi USB Bluetooth adapters](http://elinux.org/RPi_USB_Bluetooth_adapters) for buying recommendations. Trial and error is another option, since most devices cost below $10. 

### USB Hub

Raspberry PI offers limited power to USB devices (and limited number of ports). You'll need some active (powered) **USB Hub** to keep USB devices stable and working (USB Audio, USB Bluettoth and optional USB WiFi). 
Google to learn more, it's a very common topic when using Raspberry PI.

## Initial setup

The setup can be done by hand or by useing [a small installation script](https://raw.githubusercontent.com/karaambaa/a2dp-bluetooth-server/master/a2dp).

I'm using [Raspberry PI 2](https://www.raspberrypi.org/products/model-b/), running [Volumio 2](https://volumio.org). Make sure your system is up–to–date first:

```
sudo apt-get update
sudo apt-get upgrade
```

**Note:** It usually takes a while. Get some tee and sandwiches.

Then install required packages ([related article](http://www.instructables.com/id/Enhance-your-Raspberry-Pi-media-center-with-Blueto/?ALLSTEPS)):

```
sudo apt-get install alsa-utils bluez bluez-tools pulseaudio-module-bluetooth python-gobject python-gobject-2 python
```

Not quite sure it's really needed (?), but it doesn't hurt:

```
sudo usermod -a -G lp volumio
```


## Setup PulseAudi
Disable PulseAudios "auto spwan":
```
sed 's/; autospawn = yes/autospawn = no/' </etc/pulse/client.conf  >~/.config/pulse/client.conf
```
Use the following configuration to get most of PulseAudio ([related article](http://www.crazy-audio.com/2014/09/pulseaudio-on-the-raspbery-pi/)):

```
volumio@raspberrypi:~ $ nano /etc/pulse/daemon.conf
...
resample-method=ffmpeg
enable-remixing = no
enable-lfe-remixing = no
default-sample-format = s32le
default-sample-rate = 192000
alternate-sample-rate = 176000
default-sample-channels = 2
exit-idle-time = -1
...
```

**Note:** PA is pretty CPU–consuming. With the following configuration it uses ~30% of my PI's CPU.
So if you expect PI to do something else beside A2DP and avoid sound glitches, reasearch different `resample-method`.

## Setup Bluetooth

Make sure Bluetooth audio is working and discovered as a car audio system (the setup-script will use the hostname as Bluetoothname)

```
pi@raspberrypi:~ $ nano /etc/bluetooth/main.conf
[General]
Name = volumio
Class = 0x20041C
Enable = Source,Sink,Media,Socket
```

## Automating Bluetooth

To automate the Trusting and Connecting process pexpect is needed, so we have to install it by issuing the following commands.
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py
pip install pexpect
```

Download the Scripts, I put mine into a folder called `a2dp-bluetooth-server`.
```
mkdir /usr/bin/a2dp-bluetooth-server
wget https://gist.github.com/ofekp/539ce199a96e6a9ace2c1511cc7409ce/raw/30a91d80d5d7ee93e336f2e9ee1f7e2ef601e3f1/bluetoothctl.py -P /usr/bin/a2dp-bluetooth-server
wget https://raw.githubusercontent.com/karaambaa/a2dp-bluetooth-server/master/a2dp.py -P /usr/bin/a2dp-bluetooth-server
```

To enable autostarting the service we need to put the following script into `/lib/systemd/system` and enable the autostart.
```
wget https://raw.githubusercontent.com/karaambaa/a2dp-bluetooth-server/master/a2dp-server.service -P /lib/systemd/system
sudo chmod 644 /lib/systemd/system/a2dp-server.service
```
```
sudo systemctl daemon-reload
sudo systemctl enable a2dp-server.service
sudo systemctl start a2dp-server.service
```
