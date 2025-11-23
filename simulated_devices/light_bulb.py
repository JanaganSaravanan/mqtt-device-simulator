import time
from base_device import SmartDevice


class LightBulb(SmartDevice):
    def __init__(self, device_id, **kwargs):
        super().__init__(device_id, "light_bulb", **kwargs)

        self.state = {
            "power": "OFF",
            "brightness": 0
        }

        # Start telemetry loop
        self.run_loop()

    def handle_command(self, payload):
        if payload == "ON":
            self.state["power"] = "ON"
            self.state["brightness"] = 100

        elif payload == "OFF":
            self.state["power"] = "OFF"
            self.state["brightness"] = 0

        elif payload.startswith("SET "):
            try:
                value = int(payload.split()[1])
                self.state["brightness"] = max(0, min(100, value))
            except:
                pass

        self.publish_state()

    def publish_state(self):
        self.publish(f"devices/{self.device_id}/state", self.state, retain=True)

    def run_loop(self):
        def loop():
            while True:
                self.publish_state()
                time.sleep(5)

        import threading
        t = threading.Thread(target=loop)
        t.daemon = True
        t.start()

