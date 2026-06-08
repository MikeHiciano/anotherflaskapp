#import paho.mqtt.client as mqtt
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# @app.errorhandler('404')
# def errorhandler():
#     req = requests.get('https://naas.isalman.dev/no')
#     return req.json()['reason'], 404

@app.route('/')
def main():
    return 'hello there'

@app.route('/main')
def main_route():
    req = requests.get('https://naas.isalman.dev/no')
    return req.json()['reason']

if __name__ == '__main__':
    app.run(host='0.0.0.0')