from flask import Flask, request, jsonify
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'diotp2p.mooo.com'  # use the free broker from HIVEMQ
app.config['MQTT_CLIENT_ID'] = 'flaskMqttBackendNurseRedheart'
app.config['MQTT_BROKER_PORT'] = 8883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'NurseRedheart'  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = 'RgaLQFGF9Halt429'  # set the password here if the broker demands authentication
#app.config['MQTT_KEEPALIVE'] = 300  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = True  # set TLS to disabled for testing purposes

topic = '/NurseRedheart/message/json'

mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))


@app.route('/publish', methods=['POST'])
def publish_message():
   request_data = request.get_json()
   publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
   return jsonify({'code': publish_result[0]})

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)