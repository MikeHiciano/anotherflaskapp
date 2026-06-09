import paho.mqtt.client as mqtt
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def main():
    return 'hello there'

@app.route('/main')
def main_route():
    req = requests.get('https://naas.isalman.dev/no')
    return req.json()['reason']

@app.route('/message')
def message():
    client = mqtt.Client()
    client.connect('bonsamie-mqtt', 1883, 60)
    client.publish('topic/test', 'Hello MQTT')
    client.disconnect()
    return 'Message sent to MQTT broker'

if __name__ == '__main__':
    app.run(host='0.0.0.0')