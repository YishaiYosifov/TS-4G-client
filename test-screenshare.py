from common.util import send, CONFIG

import threading
import pyautogui
import keyboard
import imutils
import random
import socket
import struct
import pickle
import time
import json
import cv2
import os

def screenshare():
    screenshareSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    screenshareSocket.connect((IP, PORT))

    send(screenshareSocket, {"request_type": "login", "role": 2, "pc_name": socket.gethostname(), "password": "luka123"})
    send(screenshareSocket, {"request_type": "start_screenshare", "target_id": TARGET_ID})

    while True:
        try: data = screenshareSocket.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Server Closed")
            os._exit(0)

        if not data:
            print("Server Closed")
            os._exit(0)

        data = data.decode("utf-8")
        for action in data.split("\r"):
            if not action: continue

            action = json.loads(action)
            print(action)
            if action["request_type"] == "callback" and action["type"] == "awaiting_screenshare_client": break
        else: continue
        break
    
    threading.Thread(target=random_clicks).start()

    payloadSize = struct.calcsize("Q")
    data = b""
    while True:
        while len(data) < payloadSize:
            try: packet = screenshareSocket.recv(4096)
            except (ConnectionResetError, ConnectionAbortedError):
                print("Server Closed")
                return

            if not packet:
                print("Server Closed")
                return

            data += packet

        packedMessageSize = data[:payloadSize]
        data = data[payloadSize:]
        msg_size = struct.unpack("Q", packedMessageSize)[0]
        
        while len(data) < msg_size: data += screenshareSocket.recv(4*1024)
        frame = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame)
        frame = imutils.resize(frame, 1024)
        cv2.imshow("Receiving Video", frame)

        cv2.waitKey(1)

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

def random_clicks():
    while True:
        time.sleep(random.uniform(2, 5))
        send(s, {"request_type": "click", "target_id": TARGET_ID, "x": random.randint(0, 1080), "y": random.randint(0, 1920)})

if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+shift+z", lambda: os._exit(0))

    IP = CONFIG["ip"]
    PORT = CONFIG["port"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    print(f"Connected to {IP}:{PORT}")

    threading.Thread(target=main).start()
    send(s, {"request_type": "login", "role": 1, "pc_name": socket.gethostname(), "password": "luka123"})

    TARGET_ID = int(input())
    screenshare()

    while True: time.sleep(0.1)