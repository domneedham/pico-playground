# Pico Playground

A simple MQTT project for turning on/off the led on a Pico W.

## Setup

You will first need to make a configuration.py file containing the following keys:

```python
wlan_id = "Your SSID" # change me
wlan_password = "Your wifi password" # change me
mqtt_server = "Your mqtt server" # change me
mqtt_base_topic = "home/pico" # set to what you want
mqtt_prefix = mqtt_base_topic + "/"
```

You will need to have `ampy` installed on the host machine.

You will also need to know the device id in the system. For mac, this is something like `/dev/cu.usbmodem<xxx>`. On Linux, it will be something like `/dev/ACMtty0`. Use this in the `run` script.

You will need to setup umqtt.simple. To do this, run the `install-umqtt` script in the setup directory.

## Running

Use the `run` script passing the `--device` parameter with your device path (steps to find are above).
