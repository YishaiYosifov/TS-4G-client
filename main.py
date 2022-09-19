from common.commands import commandFunctions, init_command_functions
from common.util import *

import socket
import json
import os

IP = CONFIG["ip"]
PORT = CONFIG["port"]

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
        for request in data.split("\r"):
            if not request: continue

            if not request.endswith("}"): request += "}"
            elif not request.startswith("{"): request = "{" + request

            print(request)

            request = json.loads(request)
            if request["request_type"] == "action":
                arguments = request.copy()
                arguments.pop("request_type")
                arguments.pop("type")

                try: commandFunctions[request["type"]](*arguments.values())
                except KeyError: print(f"Unknown Action: {request['type']}")
                continue
            elif request["request_type"] == "callback":
                if request["type"] == "actions":
                    init_command_functions(request["actions"])
                    send(s, {"request_type": "login", "role": 0, "pc_name": socket.gethostname()})

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    send(s, {"request_type": "set_blocked_urls", "urls": get_blocked_urls()})
    send(s, {"request_type": "get_actions"})

    receive()