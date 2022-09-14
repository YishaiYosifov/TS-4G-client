import imutils
import socket
import pickle
import struct
import numpy
import mss
import cv2

IP  = socket.gethostbyname(socket.gethostname())
PORT = 9999

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("0.0.0.0", PORT))
s.listen(1)

print(f"Server started on {IP}:{PORT}")

while True:
    connection, address = s.accept()
    print(f"Received a connection from {address[0]}{address[1]}")
    
    with mss.mss() as screen:
        resize = int(screen.monitors[1]["width"] / 2)
        if resize > 800: resize = 800
        
        while True:
            frame = screen.grab(screen.monitors[1])

            frame = cv2.cvtColor(numpy.asarray(frame), cv2.COLOR_RGB2BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width=resize)
            pickledFrame = pickle.dumps(frame)
            
            message = struct.pack("Q", len(pickledFrame)) + pickledFrame
            connection.sendall(message)
            
            key = cv2.waitKey(1) & 0xFF
            if key== ord("q"): connection.close()