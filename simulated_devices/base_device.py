import json
import time
import threading
import paho.mqtt.client as mqtt


class SmartDevice:
    def __init__(self, device_id, device_type, broker="localhost", port=1883,
                 username='admin', password='admin123'):

        self.device_id = device_id
        self.device_type = device_type
        self.state = {}  # device-specific state

        self.client = mqtt.Client(client_id=device_id, clean_session=False)

        # authentication
        if username and password:
            self.client.username_pw_set(username, password)

        # LWT
        self.client.will_set(
            f"devices/{self.device_id}/status",
            payload="offline",
            retain=True
        )

        # callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(broker, port, keepalive=30)

        # Background network loop
        self.thread = threading.Thread(target=self.client.loop_forever)
        self.thread.daemon = True
        self.thread.start()

    # ---------------- CALLBACKS ---------------- #

    def on_connect(self, client, userdata, flags, rc):
        print(f"[{self.device_id}] Connected with result code {rc}")

        # Device is online
        client.publish(
            f"devices/{self.device_id}/status",
            "online",
            retain=True
        )

        # Subscribe to commands
        client.subscribe(f"devices/{self.device_id}/command")

    def on_disconnect(self, client, userdata, rc):
        print(f"[{self.device_id}] Disconnected: {rc}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"[{self.device_id}] Command received:", payload)
        self.handle_command(payload)

    # ---------------- DEVICE LOGIC ---------------- #

    def handle_command(self, payload):
        """Override in child classes"""
        pass

    def publish(self, topic, data, retain=False):
        payload = json.dumps(data)
        self.client.publish(topic, payload, retain=retain)

    def publish_state(self):
        """Override in child classes"""
        pass

