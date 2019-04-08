import socket
import psycopg2
import psycopg2.extras
from datetime import datetime
from config import POSTGRESS_CONNECTION_STRING, MQTT_BROKER_HOST, MQTT_PORT,EMULATOR_PORTS, CLIENT_ID
import paho.mqtt.client as paho
import time
import decimal

HEADERSIZE = 10


def insert_to_DB(cursor, data):
	cursor.execute( """INSERT INTO telemetry.telemetry (data_key, data_value) VALUES (%s, %s) RETURNING *""", (data[0], data[1]))
	data = cursor.fetchone()
	data['client_id'] = CLIENT_ID
	data['created_at'] = str(data['created_at'])
	return data
def mqtt_on_publish(client,userdata,result):
    # print("Device 1 : Data published.")
    pass

def init_db_connection(connection_string=POSTGRESS_CONNECTION_STRING):
	db_connectioin = psycopg2.connect(connection_string)
	db_cursor = db_connectioin.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	return db_connectioin, db_cursor

def init_socket_connection(emulator_type):
	# connect to emitter
	s = socket.socket()
	host = socket.gethostname()  # or just use (host = '')
	port = EMULATOR_PORTS[emulator_type]
	s.connect((host, port))
	return s

def init_mqtt_client(broker,port):
	client= paho.Client("admin")
	client.on_publish = mqtt_on_publish
	client.connect(broker,port)
	return client

def main():
	db_connection, db_cursor = init_db_connection()
	temperature_socket_connection = init_socket_connection('temperature')
	mqtt_client = init_mqtt_client(broker=MQTT_BROKER_HOST, port=MQTT_PORT)
	hashtag = f'/telemetry/client/{CLIENT_ID}/'
	print(hashtag)

	while True:
		temperature_data = temperature_socket_connection.recv(16)
		
		if temperature_data:
			temperature_data = int(temperature_data[:HEADERSIZE].decode("utf-8"))
			advanced_data = insert_to_DB(db_cursor, ('temperature',temperature_data))
			db_connection.commit()
			# send to mqtt
			ret = mqtt_client.publish(hashtag,str(advanced_data))
			print(str(advanced_data))
		

if __name__ == "__main__":
    main()
