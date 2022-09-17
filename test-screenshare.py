import common.util
import threading
import keyboard
import imutils
import socket
import struct
import pickle
import time
import json
import cv2
import os

def main():
    while True:
        try: data = s.recv(1024)
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
            if action["request_type"] == "callback" and action["type"] == "awaiting_screenshare_client": break
        else: continue
        break
    
    payloadSize = struct.calcsize("Q")
    data = b""
    while True:
        while len(data) < payloadSize:
            try: packet = s.recv(4096)
            except (ConnectionResetError, ConnectionAbortedError):
                print("Server Closed")
                os._exit(0)

            if not packet:
                print("Server Closed")
                os._exit(0)

            data += packet

        packedMessageSize = data[:payloadSize]
        data = data[payloadSize:]
        msg_size = struct.unpack("Q", packedMessageSize)[0]
        
        while len(data) < msg_size: data += s.recv(4*1024)
        frame = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame)
        frame = imutils.resize(frame, 1024)
        cv2.imshow("Receiving Video", frame)

        cv2.waitKey(1)

if __name__ == "__main__":
    keyboard.add_hotkey("ctrl+shift+z", lambda: os._exit(0))

    IP = "127.0.0.1"
    PORT = 1414

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    print(f"Connected to {IP}:{PORT}")

    threading.Thread(target=main).start()
    common.util.send(s, {"request_type": "login", "role": 2, "pc_name": socket.gethostname(), "password": "luka123"})
    common.util.send(s, {"request_type": "start_screenshare", "target_id": int(input())})

    while True: time.sleep(0.1)