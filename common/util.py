import threading
import tkinter
import socket
import json

def send(s : socket.socket, data : dict): s.send(json.dumps(data).encode("utf-8"))

class BlockScreen(threading.Thread):
    def __init__(self): threading.Thread.__init__(self)
    
    def close(self): self.root.quit()
    
    def run(self):
        self.root = tkinter.Tk()
        self.root.configure(background="black")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.mainloop()

blockScreen = BlockScreen()