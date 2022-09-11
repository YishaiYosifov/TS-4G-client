import socket
import json

with open("config.json", "r") as f: config = json.load(f)
IP = config["ip"]
PORT = config["port"]

def main():
    while True:
        try: data = s.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Server Closed")
            exit()

        if not data:
            print("Server Closed")
            exit()

        print(data)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))