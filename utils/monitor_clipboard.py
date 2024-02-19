import pyperclip
import time
import threading
from utils.socket_connect import *

# Event object used to signal threads to stop
stop_event = threading.Event()


def monitor_clipboard(polling_interval=1.0):
    last_clipboard_content = None
    try:
        while not stop_event.is_set():
            clipboard_content = pyperclip.paste()
            if clipboard_content != last_clipboard_content:
                print("Clipboard data:", clipboard_content)
                if (clipboard_content.__len__() < 100):
                    # Send data to server
                    sio.emit('clipboard_data', clipboard_content)
                last_clipboard_content = clipboard_content
            time.sleep(polling_interval)
    except KeyboardInterrupt:
        print("Clipboard monitoring stopped.")
