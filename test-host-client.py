from common.util import *

import threading
import keyboard
import socket
import time
import json
import os

with open("config.json", "r") as f: config = json.load(f)
IP = config["ip"]
PORT = config["port"]

def temp_send_request():
    while True: s.send(input().encode("utf-8"))

def main():
    while True:
        try: data = s.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Server Closed")
            os._exit(0)

        if not data:
            print("Server Closed")
            os._exit(0)

        print(data)

if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+shift+z", lambda: os._exit(0))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    print(f"Connected to {IP}:{PORT}")

    threading.Thread(target=main).start()

    send(s, {"request_type": "login", "role": 1, "pc_name": socket.gethostname(), "password": "luka123"})

    """target = int(input())
    send(s, {"request_type": "block_input", "target_id": target})
    time.sleep(5)
    send(s, {"request_type": "unblock_input", "target_id": target})"""

    temp_send_request()