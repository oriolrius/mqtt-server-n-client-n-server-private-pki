import os
import sys
import ssl
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

def main(topic: str, message: str):
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve MQTT and SSL/TLS configurations from environment variables
    MQTT_HOST = os.getenv('MQTT_HOST')
    MQTT_PORT = int(os.getenv('MQTT_PORT', 8883))

    MQTT_CLIENT_CA = os.getenv('MQTT_CLIENT_CA') 
    MQTT_CLIENT_CERT = os.getenv('MQTT_CLIENT_CERT')
    MQTT_CLIENT_KEY = os.getenv('MQTT_CLIENT_KEY')
    MQTT_CLIENT_PASSPHRASE = os.getenv('MQTT_CLIENT_PASSPHRASE')

    # Validate required parameters
    required_vars = [MQTT_HOST, MQTT_PORT, MQTT_CLIENT_CA, MQTT_CLIENT_CERT, MQTT_CLIENT_KEY, MQTT_CLIENT_PASSPHRASE]
    if not all(required_vars):
        print("Error: Missing one or more required environment variables.")
        sys.exit(1)

    # Create an MQTT client instance
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )

    # Set up TLS
    client.tls_set(
        ca_certs=MQTT_CLIENT_CA,
        certfile=MQTT_CLIENT_CERT,
        keyfile=MQTT_CLIENT_KEY,
        keyfile_password=MQTT_CLIENT_PASSPHRASE,
        cert_reqs=ssl.CERT_REQUIRED
    )

    # Define callback functions
    def on_connect(client, userdata, flags, rc, properties=None):  # Added properties parameter
        if rc == 0:
            print("Connected to MQTT Broker successfully.")
            # Publish the message once connected
            result = client.publish(topic, message)
            status = result[0]
            if status == 0:
                print(f"Message '{message}' sent to topic '{topic}'.")
            else:
                print(f"Failed to send message to topic {topic}.")
            client.disconnect()
        else:
            print(f"Failed to connect, return code {rc}")

    # Assign callbacks
    client.on_connect = on_connect

    # Connect to the MQTT broker
    try:
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # Start the network loop and wait for callbacks
    client.loop_forever()

if __name__ == "__main__":
    main("topic1", "message1")
