from light_bulb import LightBulb
import time

USER = "admin"
PASS = "admin123"

# Device instances
light = LightBulb(
    "light_1",
    broker="localhost",
    port=1883,
    username=USER,
    password=PASS
)

print("Simulated devices started...")

while True:
    time.sleep(60)

