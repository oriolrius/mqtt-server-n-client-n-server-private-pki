# Load environment variables from .env file
set dotenv-load
# mqttx-cli using docker
mqttx-cli := 'docker run --rm \
  --entrypoint /usr/local/bin/mqttx \
  -v ./${MQTT_CLIENT_CA}:/tmp/ca.crt \
  -v ./${MQTT_CLIENT_CERT}:/tmp/client.example.tld.crt \
  -v ./${MQTT_CLIENT_KEY}:/tmp/client.example.tld.key \
  emqx/mqttx-cli'

mqtt:
  cd mosquitto && mosquitto -c mosquitto.conf

ssl_client:
  openssl s_client \
      -CAfile ${MQTT_CLIENT_CA} \
      ${MQTT_HOST}:${MQTT_PORT}

ssl_client_cert:
  openssl s_client \
      -CAfile ${MQTT_CLIENT_CA} \
      --cert ${MQTT_CLIENT_CERT} \
      --key ${MQTT_CLIENT_KEY} \
      ${MQTT_HOST}:${MQTT_PORT}

mosquitto_pub +ARGS:
  mosquitto_pub \
      --cafile ${MQTT_CLIENT_CA} \
      --cert ${MQTT_CLIENT_CERT} \
      --key ${MQTT_CLIENT_KEY} \
      -d -h ${MQTT_HOST} -p ${MQTT_PORT} \
      -t topic1 -m "message1" {{ ARGS }}

mosquitto_sub +ARGS:
  mosquitto_sub \
      --cafile ${MQTT_CLIENT_CA} \
      --cert ${MQTT_CLIENT_CERT} \
      --key ${MQTT_CLIENT_KEY} \
      -d -h ${MQTT_HOST} -p ${MQTT_PORT} \
      -v -t topic1 {{ ARGS }}

mqttx_sub:
  {{mqttx-cli}} sub \
    --ca /tmp/ca.crt \
    --cert /tmp/client.example.tld.crt \
    --key /tmp/client.example.tld.key \
    -h mqtt.example.tld \
    -p 8884 -l wss \
    -t topic1

mqttx_pub:
  {{mqttx-cli}} pub \
    --ca /tmp/ca.crt \
    --cert /tmp/client.example.tld.crt \
    --key /tmp/client.example.tld.key \
    -h mqtt.example.tld \
    -p 8883 -l mqtts \
    -t topic1 -m message1

install_uv:
  curl -LsSf https://astral.sh/uv/install.sh | sh

sync:
  uv sync
  
py_pub:
  uv run python_client/mqtt_pub.py

py_sub:
  uv run python_client/mqtt_sub.py
