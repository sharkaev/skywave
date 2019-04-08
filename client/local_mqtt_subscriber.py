import psycopg2
import psycopg2.extras
import yaml
from config import POSTGRESS_CONNECTION_STRING, MQTT_BROKER_HOST, MQTT_PORT, CLIENT_ID
import paho.mqtt.client as mqtt
import os
import subprocess


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    hashtag = f'/telemetry/client/{CLIENT_ID}/'
    print(hashtag)
    # call subprocess
    cmd = 'py handle_connection.py'
    # subprocess.call(['py','handle_connection.py'], shell=True)
    client.subscribe(hashtag)
    os.system(cmd)
    # os.system(cmd)


def on_message(client, userdata, msg):
    # delete from localDB
    global db_connectioin, db_cursor 
    data = yaml.load(msg.payload.decode())
    try:
        db_cursor.execute("""DELETE from telemetry.telemtry WHERE id = %s""",(data['id'],))
        db_connectioin.commit()
        # print("Deleted data with id", data['id'])
    except Exception as e:
        print(e)

def init_local_mqtt_subscriber():
    client = mqtt.Client()
    client.connect(MQTT_BROKER_HOST, MQTT_PORT, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    return client

def init_db_connection(connection_string=POSTGRESS_CONNECTION_STRING):
	db_connectioin = psycopg2.connect(connection_string)
	db_cursor = db_connectioin.cursor()
	return db_connectioin, db_cursor

def main():
    local_mqtt_subscriber = init_local_mqtt_subscriber()
    local_mqtt_subscriber.loop_forever()

if __name__ == "__main__":
    db_connectioin, db_cursor= init_db_connection()
    main()


