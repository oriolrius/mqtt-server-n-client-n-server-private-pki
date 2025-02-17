import os
import sys
import ssl
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get configuration from environment variables
    MQTT_HOST = os.getenv('MQTT_HOST')
    MQTT_PORT = int(os.getenv('MQTT_PORT', 8883))
    
    MQTT_CLIENT_CA = os.getenv('MQTT_CLIENT_CA') 
    MQTT_CLIENT_CERT = os.getenv('MQTT_CLIENT_CERT')
    MQTT_CLIENT_KEY = os.getenv('MQTT_CLIENT_KEY')
    MQTT_CLIENT_PASSPHRASE = os.getenv('MQTT_CLIENT_PASSPHRASE')

    # Topic to subscribe to
    TOPIC = "topic1"  # Subscribes to all topics
    
    # Validate required parameters
    required_vars = [MQTT_HOST, MQTT_PORT, MQTT_CLIENT_CA, MQTT_CLIENT_CERT, MQTT_CLIENT_KEY, MQTT_CLIENT_PASSPHRASE]
    if not all(required_vars):
        print("Error: Missing one or more required environment variables.")
        sys.exit(1)

    # Callback when a message is received
    def on_message(client, userdata, msg):
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    # Callback for successful connection
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker successfully.")
            client.subscribe(TOPIC)
            print(f"Subscribed to topic: {TOPIC}")
        else:
            print(f"Failed to connect. Return code: {rc}")

    # Create MQTT client
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

    # Assign callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        # Connect to broker
        client.connect(MQTT_HOST, MQTT_PORT)
        # Start the loop
        client.loop_forever()
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()