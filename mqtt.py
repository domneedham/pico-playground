import time
from led import LED
from umqtt.simple import MQTTClient
from configuration import mqtt_server, mqtt_prefix, mqtt_base_topic
from util import singleton


@singleton
class MQTT:
    class MQTT_Callback:
        def __init__(self, topic, callback) -> None:
            self.topic = topic
            self.callback = callback

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.lastping = 0
        self.registered_callbacks = []
        self.client = MQTTClient(mqtt_prefix, mqtt_server, user=None,
                                 password=None, keepalive=300, ssl=False, ssl_params={})
        self.connect()
        scheduler.schedule("mqtt-heartbeat", 250,
                           self.scheduler_heartbeat_callback)
        scheduler.schedule("mqtt-check", 1, self.scheduler_mqtt_callback)

    def connect(self):
        print("Connecting to MQTT")
        self.client.connect()
        self.heartbeat(True)
        self.client.set_callback(self.mqtt_callback)
        topic = mqtt_prefix + "#"
        self.client.subscribe(topic)
        print("Subscribed to " + topic)

    def heartbeat(self, first=False):
        if first:
            self.client.ping()
            self.lastping = time.ticks_ms()
        if time.ticks_diff(time.ticks_ms(), self.lastping) >= 300000:
            self.client.ping()
            self.lastping = time.ticks_ms()
        return

    def scheduler_heartbeat_callback(self, t):
        self.heartbeat(False)

    def scheduler_mqtt_callback(self, t):
        self.client.check_msg()

    def mqtt_callback(self, topic, msg):
        t = topic.decode().lstrip(mqtt_prefix)
        for c in self.registered_callbacks:
            if t == c.topic:
                c.callback(topic, msg)

    def send_event(self, topic, msg):
        if topic == "":
            topic = mqtt_base_topic
        else:
            topic = mqtt_prefix + topic
        self.client.publish(topic, msg)

    def register_topic_callback(self, topic, callback):
        self.registered_callbacks.append(self.MQTT_Callback(topic, callback))
