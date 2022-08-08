from machine import Pin
from mqtt import MQTT
from scheduler import Scheduler
from util import singleton


@singleton
class LED:
    def __init__(self, scheduler: Scheduler, mqtt: MQTT):
        self.scheduler = scheduler
        self.mqtt = mqtt
        self.led = Pin("LED", Pin.OUT)
        mqtt.register_topic_callback("set", self.mqtt_set_state_callback)
        mqtt.register_state_callback("state", self.mqtt_state_callback)

    def toggle(self):
        self.led.toggle()
        self.publish_state()

    def turn_on(self):
        self.led.value(1)
        self.publish_state()

    def turn_off(self):
        self.led.value(0)
        self.publish_state()

    def is_on(self):
        return self.led.value() == 1

    def is_off(self):
        return self.led.value() == 0

    def led_toggle_callback(self, t):
        self.toggle()

    def mqtt_set_state_callback(self, topic, msg):
        if msg == b'{"state": "ON"}':
            self.turn_on()
        elif msg == b'{"state": "OFF"}':
            self.turn_off()

    def publish_state(self):
        self.mqtt.send_state()

    def get_state(self):
        state = "OFF"
        if self.is_on():
            state = "ON"
        return state

    def mqtt_state_callback(self):
        state = self.get_state()
        return str(state)
