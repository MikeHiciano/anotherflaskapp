from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from flask import Flask, jsonify
import psycopg2
import requests
import os

load_dotenv()
app = Flask(__name__)

class Server:
    def __init__(self):
        pass

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

class db:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        self.cur = self.conn.cursor()

    @app.route('/db', methods=['GET', 'POST'])
    def create_db():
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id SERIAL PRIMARY KEY,
                device VARCHAR(100),
                mac_address VARCHAR(100),
                temperature FLOAT,
                humidity FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        self.conn.commit()
        return 'Database and table created'
    
    def insert_db(self, device, mac_address, temperature, humidity):
        self.cur.execute("INSERT INTO sensor_data (device, mac_address, temperature, humidity) VALUES (%s, %s, %s, %s);", (device, mac_address, temperature, humidity))
        self.conn.commit()
        self.conn.close()
        return 'Sensor data inserted into database'
    
    def get_db(self):
        self.cur.execute("SELECT * FROM sensor_data;")
        rows = self.cur.fetchall()
        self.conn.close()

        if method == 'GET':
            return jsonify(rows)
            
if __name__ == '__main__':
    server = Server()
    server.app.run(host='0.0.0.0')