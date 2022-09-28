from flask import Flask
from flask import Flask, request, json, jsonify
from flask_mqtt import Mqtt
from concurrent.futures import thread
import ssl

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'diotp2p.mooo.com'  # use the free broker from HIVEMQ
app.config['MQTT_CLIENT_ID'] = 'flaskMqttBackendNurseRedheart'
app.config['MQTT_BROKER_PORT'] = 8883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = 'NurseRedheart'  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = 'RgaLQFGF9Halt429'  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 300  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = True  # set TLS to disabled for testing purposes
app.config["MQTT_TLS_VERSION"] = ssl.PROTOCOL_TLS_CLIENT

mqtt = Mqtt(app)

topic = 'NurseRedheart/message/json'

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/sensors/air-quality/co2", methods = ['GET'])
def getCo2Readings():
    #get latest from database

    CO2 = 400
    return json.dumps({'status':'OK', 'CO2': CO2}, ensure_ascii=False)

@app.route("/sensors/air-quality/tvoc", methods = ['Get'])
def getTvocReadings():
    #get latest from database
    tvoc = 400
    return json.dumps({'status':'OK', 'tvoc': tvoc}, ensure_ascii=False)

@app.route("/actuator/leds/1", methods = ['GET'])
def modifyLedState():
    #send MQTT message with json body with new LED state
    mqtt.publish('NurseRedheart/message/json', 'hi from flask')
    return json.dumps({'status':'OK'}, ensure_ascii=False)



if __name__ == "__main__":
    app.run(debug=True)
