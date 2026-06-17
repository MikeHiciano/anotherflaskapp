from dotenv import load_dotenv
from paho.mqtt import client, subscribe
from flask import Flask, jsonify
import json
import threading
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
        client = Client()
        client.connect('test.mosquitto.org', 1883, 60)
        client.publish(os.getenv('mqtt_topic'), 'Hello MQTT')
        client.disconnect()
        return 'Message sent to MQTT broker'
    
    def subscribe_mqtt(self):
        #client.connect('test.mosquitto.org', 1883, 60)
        msg = subscribe.simple(os.getenv('mqtt_topic'), hostname='test.mosquitto.org')
        msg = json.loads(msg.payload.decode('utf-8'))
        db_instance = db()
        db_instance.insert_db(
            device= msg.get("device"),
            mac_address=msg.get("mac_address"),
            temperature=msg.get("temperature"),
            humidity=msg.get ("humidity"))

class db():
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        self.cur = self.conn.cursor()

    @app.route('/db')
    def create_db():
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        cur = conn.cursor()               
        cur.execute('''
                        CREATE TABLE IF NOT EXISTS sensor_data (id SERIAL PRIMARY KEY, 
                                                                device VARCHAR(100), 
                                                                mac_address VARCHAR(100), 
                                                                temperature FLOAT, 
                                                                humidity FLOAT, 
                                                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                        ''')
        conn.commit()
        return 'Database and table created'
    
    def check_db_exists(self):
        self.cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sensor_data');")
        exists = self.cur.fetchone()[0]
        self.conn.close()
        return exists
    
    def insert_db(self, device, mac_address, temperature, humidity):
        self.cur.execute("INSERT INTO sensor_data (device, mac_address, temperature, humidity) VALUES (%s, %s, %s, %s);", (device, mac_address, temperature, humidity))
        self.conn.commit()
        self.conn.close()
        return 'Sensor data inserted into database'
    
    @app.route('/get_db')
    def get_db():
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM sensor_data;")
        rows = cur.fetchall()
        conn.close()

        return jsonify(rows)
            
if __name__ == '__main__':

        server = Server()
        mqtt_thread = threading.Thread(target=server.subscribe_mqtt)
        server_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
        mqtt_thread.start()
        server_thread.start()
    

  
    