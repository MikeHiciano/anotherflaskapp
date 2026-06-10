from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from flask import Flask, jsonify
import psycopg2
import requests
import os

load_dotenv()
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
    client.connect('test.mosquitto.org', 1883, 60)
    client.publish(os.getenv('mqtt_topic'), 'Hello MQTT')
    client.disconnect()
    return 'Message sent to MQTT broker'

@app.route('/db')
def db():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0')