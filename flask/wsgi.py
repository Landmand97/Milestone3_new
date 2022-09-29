import string
from flask import Flask, request, json, jsonify, Request
from flask_mqtt import Mqtt
from concurrent.futures import thread
import ssl
from readingsDB import *

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

topic = '#'

sensorReadings = {'CO2': 0, 'TVOC': 0}

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=json.loads(message.payload.decode())
  )
   print('Received msg on topic: {topic} with payload: {payload}'.format(**data))
   if data['topic'] == 'NurseRedheart/test/airquality/json':
    sensorReadings.update(data['payload'])
    readingsDB.postReadingsToDB(data['payload'])


@app.route("/")
def hello_world():
    CO2readings = readingsDB.printReadings('CO2')
    CO2Table = produceReadingsTable('CO2',CO2readings)
    TVOCreadings = readingsDB.printReadings('TVOC')
    TVOCTable = produceReadingsTable('TVOC',TVOCreadings)
    return CO2Table + TVOCTable
    

def produceReadingsTable(sensor,readings):
    output = "<table> <tr> <th>{}-Value</th> <th> TIME</th> </tr>".format(sensor)
    for x in reversed(range(len(readings))):
      output = output + "<tr> <td>" + str(readings[x][0]) + "</td> <td>" + str(readings[x][1]) + "</td> </tr>"
    output = output + "</table>"
    return output

@app.route("/sensors/air-quality/co2", methods = ['GET'])
def getCo2Readings():
    return json.dumps({'status':'OK', 'CO2':sensorReadings['CO2']}, ensure_ascii=False)

@app.route("/sensors/air-quality/tvoc", methods = ['Get'])
def getTvocReadings():  
    return json.dumps({'status':'OK', 'TVOC': sensorReadings['TVOC']}, ensure_ascii=False)

@app.route("/actuator/leds/1", methods = ['GET'])
def modifyLedState():
    #send MQTT message with json body with new LED state
    side = request.args.get('side')
    R = request.args.get('R')
    G = request.args.get('G')
    B = request.args.get('B')
    if side == 'both':
        setRGB('left',R,G,B)
        setRGB('right',R,G,B)
    else:
        setRGB(side,R,G,B)
       
    return json.dumps({'status':'OK'}, ensure_ascii=False)

def setRGB(side=string, R=int, G=int, B= int):
    mqtt.publish('NurseRedheart/Actuators/LEDs/{}/R/json'.format(side), R)
    mqtt.publish('NurseRedheart/Actuators/LEDs/{}/G/json'.format(side), G)
    mqtt.publish('NurseRedheart/Actuators/LEDs/{}/B/json'.format(side), B)


readingsDB = readingsDB()
readingsDB.createDBTables()

if __name__ == "__main__":
    app.run(debug=True)
