import paho.mqtt.client as mqtt
from clickhouse_driver import Client
import yaml
# This is the Subscriber
# hostname
broker = "localhost"
# port
port = 1883
# time to live
timelive = 60


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/telemetry/client/+/")


def on_message(client, userdata, msg):
    global db_client
    data = yaml.load(msg.payload.decode())
    data['created_at'] = float(data['created_at'])
    data['data_value'] = int(data['data_value'])
    del data['id']
    print(msg.payload.decode())
    try:
        db_client.execute("INSERT INTO telemetry.telemetry(client_id, created_at, data_key, data_value) VALUES",[data], with_column_types=True )
    except Exception as e:
        print(e)
    # insert to db

def init_mqtt_client():
    client = mqtt.Client()
    client.connect(broker, port, timelive)
    client.on_connect = on_connect
    client.on_message = on_message
    return client

def init_db_connection():
    return Client('localhost')

def main():
    mqtt_client = init_mqtt_client()
    mqtt_client.loop_forever()

if __name__ == "__main__":
    db_client = init_db_connection()
    x = db_client.execute('SHOW DATABASES')
    print(x)
    main()


