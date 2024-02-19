import sched
import time
import socketio
from datetime import datetime, timezone
from utils.get_mac_address import get_mac_address

# Initialize Socket.IO client with reconnection settings
sio = socketio.Client(logger=True, engineio_logger=True, reconnection=True,
                      reconnection_attempts=None, reconnection_delay=1, reconnection_delay_max=5)

scheduler = sched.scheduler(time.time, time.sleep)
new_server_url = None


# Event handler for successful connection
@sio.event
def connect():
    print("Successfully connected to the server.")
    # If categorizing Python clients, emit their type here
    sio.emit('register_client_type', {'type': 'python'})
    # Send the MAC address to the server upon the initial connection
    mac_address = get_mac_address()
    sio.emit('register_login', mac_address)
    print(f"MAC address {mac_address} sent to server.")


@sio.event
def disconnect():
    print("Disconnected from server")    

# Event handler for reconnection


@sio.event
def reconnect():
    print("Successfully reconnected to the server.")


def connect_to_server(server_url):
    while True:
        try:
            sio.connect(server_url)
            if sio.connected:
                print("Connected to server.")
                break  # Exit loop if connected
        except socketio.exceptions.ConnectionError:
            print("Connection failed, retrying...")
            time.sleep(5)  # Wait before retrying to connect


@sio.event
def updateServerInfo(data):
    global new_server_url
    new_server_url = f'http://{data["newIp"]}'  # Construct the new server URL
    restart_time_str = data["restartTime"]
    restart_time = datetime.strptime(restart_time_str, '%Y-%m-%dT%H:%M:%SZ')
    restart_time = restart_time.replace(tzinfo=timezone.utc).astimezone(
        tz=None)  # Convert to local time if needed
    current_time = datetime.now()
    delay = (restart_time - current_time).total_seconds()
    if delay > 0:
        print(f"Scheduled to reconnect to {new_server_url} at {restart_time}")
        scheduler.enter(delay, 1, reconnect_to_new_server)


def reconnect_to_new_server():
    print(f"Reconnecting to new server: {new_server_url}")
    sio.disconnect()
    sio.connect(new_server_url)
