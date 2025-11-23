import paho.mqtt.client as mqtt
import threading
import time

BROKER = "localhost"
PORT = 1883
USERNAME = "admin"
PASSWORD = "admin123"

# Store latest device state.
device_state = {}

# -------------------------------------------------------------------
# MQTT CALLBACKS
# -------------------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ Connected to MQTT")
        client.subscribe("devices/#")
        print("✓ Subscribed to devices/#")
    else:
        print("✗ Failed to connect:", rc)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"[MQTT] {topic} = {payload}")

    # Example topic: devices/light_1/state
    parts = topic.split("/")
    if len(parts) < 3:
        return

    _, device, prop = parts  # devices/light_1/state
    if device not in device_state:
        device_state[device] = {}

    device_state[device][prop] = payload


def on_disconnect(client, userdata, rc):
    print("⚠ Disconnected from broker. Reconnecting...")
    time.sleep(1)


# -------------------------------------------------------------------
# MQTT START
# -------------------------------------------------------------------
def start_mqtt():
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connect(BROKER, PORT, keepalive=60)

    # Run network loop in background
    t = threading.Thread(target=client.loop_forever)
    t.daemon = True
    t.start()

    return client


# -------------------------------------------------------------------
# SEND COMMAND
# -------------------------------------------------------------------
def send_command(client, device, command):
    topic = f"devices/{device}/command"
    client.publish(topic, command)
    print(f"→ Published to {topic}: {command}")


# -------------------------------------------------------------------
# SIMPLE MENU
# -------------------------------------------------------------------
def menu_loop(client):
    while True:
        print("\n=== CONTROL PANEL ===")
        print("Device States:")
        for dev, props in device_state.items():
            print(f"  {dev}: {props}")

        print("\nActions:")
        print("1. Turn ON light_1")
        print("2. Turn OFF light_1")
        print("3. Refresh")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            send_command(client, "light_1", "ON")

        elif choice == "2":
            send_command(client, "light_1", "OFF")

        elif choice == "3":
            continue

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
if __name__ == "__main__":
    client = start_mqtt()
    time.sleep(1)
    menu_loop(client)

