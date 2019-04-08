import subprocess
if __name__ == "__main__":
    subprocess.call('py emitter_listener.py', shell=True)
    subprocess.call('py local_mqtt_subscriber.py', shell=True)
