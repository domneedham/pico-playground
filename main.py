from led import LED
from mqtt import MQTT
from pico_temperature import PicoTemperature
from wlan import WLAN
from scheduler import Scheduler

print("-" * 15)
print("PICO PLAYGROUND")
print("-" * 15)

print("Configuring...")
scheduler = Scheduler()
wlan = WLAN(scheduler)
mqtt = MQTT(scheduler)
led = LED(scheduler, mqtt)
pico_temperature = PicoTemperature(scheduler, mqtt)
print("Configured")

print("")
print("Starting...")
scheduler.start()
