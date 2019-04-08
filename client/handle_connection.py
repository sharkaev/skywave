import psycopg2
import psycopg2.extras
import paho.mqtt.client as paho

import yaml
from config import POSTGRESS_CONNECTION_STRING, MQTT_BROKER_HOST, MQTT_PORT, CLIENT_ID
import paho.mqtt.client as mqtt



def init_db_connection(connection_string=POSTGRESS_CONNECTION_STRING):
	db_connectioin = psycopg2.connect(connection_string)
	db_cursor = db_connectioin.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	return db_connectioin, db_cursor

def mqtt_on_publish(client,userdata,result):
    # print("Device 1 : All Saved data is published.")
    pass

def init_mqtt_client(broker,port):
	client= paho.Client("admin")
	client.on_publish = mqtt_on_publish
	client.connect(broker,port)
	return client


def main():
    print("callled  in main")
    db_connection, db_cursor = init_db_connection()
    mqtt_client = init_mqtt_client(broker=MQTT_BROKER_HOST, port=MQTT_PORT)
    hashtag = f'/telemetry/client/{CLIENT_ID}/'
    db_cursor.execute("""SELECT * FROM telemetry.telemetry""")
    data = db_cursor.fetchall()
    for i in data:
        # i['created_at'] = i['created_at'].strftime('%Y-%m-%d %H:%M:%S.%f')
        # print(i)
        ret= mqtt_client.publish(hashtag,str(i))

if __name__ == "__main__":

    main()
print("callled global")