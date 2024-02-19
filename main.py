from utils.monitor_clipboard import *
from utils.get_mac_address import *
from utils.socket_connect import *
import time
import threading
import keyboard


def cal():
    while not stop_event.is_set():
        # Your cal() logic here
        print("ssss")
        time.sleep(1)


def check_for_exit_combination():
    while True:
        if keyboard.is_pressed('ctrl+alt+shift+e'):
            print("Exit key combination detected. Stopping threads...")
            mac_address = get_mac_address()
            sio.emit('logout', mac_address)
            sio.disconnect()
            stop_event.set()  # Signal all threads to stop
            break
        time.sleep(0.1)


if __name__ == "__main__":
    # Ensure this matches your Socket.IO server address
    server_url = 'http://192.168.133.112:8080'
    connect_to_server(server_url)
    # scheduler.run()
    print("Monitoring clipboard for changes. Press Ctrl+C to stop.")
    print("Press Ctrl+Alt+Shift+E to stop.")
    print("---------------------------------------------------")

    # Since get_mac_address likely only needs to be run once, call it directly
    # If it needs to be in a continuous loop, consider wrapping it in a function with a loop and using a thread as with monitor_clipboard
    mac_address = get_mac_address()
    print("MAC address:", mac_address)

    # Create a thread for clipboard monitoring
    clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    # cal_thread = threading.Thread(target=cal, daemon=True)

    clipboard_thread.start()
    # cal_thread.start()

    # Start a non-daemon thread to check for the exit key combination
    # This thread will keep the application alive until the combination is pressed
    exit_thread = threading.Thread(target=check_for_exit_combination)
    exit_thread.start()

    # Wait for the exit thread to finish before exiting the program
    exit_thread.join()
