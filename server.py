#import paho.mqtt.client as mqtt
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def main():
    req = requests.get('https://naas.isalman.dev/no')
    return req.json()['reason']

if __name__ == '__main__':
    app.run()