from common.util import *

import common.actions as actions
import socket
import json
import os

with open("config.json", "r") as f: config = json.load(f)
IP = config["ip"]
PORT = config["port"]

def receive():
    print(f"Connected to {IP}:{PORT}")
    while True:
        try: data = s.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Server Clsosed")
            os._exit(0)

        if not data:
            print("Server Closed")
            os._exit(0)

        print(data)
        data = json.loads(data.decode("utf-8"))
        if data["request_type"] == "action":
            try: actionFunctions[data["type"]]()
            except KeyError: print(f"Unknown Action: {data['type']}")
            continue

if __name__ == "__main__":
    actionFunctions = {}
    for file in os.listdir("common/actions"):
        if file == "__init__.py" or os.path.isdir(f"common/actions/{file}"): continue

        file = file.removesuffix(".py")
        actionFunctions[file] = getattr(actions, file)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    receive()