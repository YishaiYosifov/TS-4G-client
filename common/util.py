import ctypes
import socket
import json

def send(s : socket.socket, data : dict): s.send(json.dumps(data).encode("utf-8"))

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

with open("config.json", "r") as f: CONFIG = json.load(f)
