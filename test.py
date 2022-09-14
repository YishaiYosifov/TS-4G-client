import imutils
import socket
import pickle
import struct
import cv2

IP = "192.168.56.1"
PORT = 9999

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((IP, PORT))

payloadSize = struct.calcsize("Q")
data = b""
while True:
    while len(data) < payloadSize:
        packet = s.recv(4096)
        if not packet: break
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

    if cv2.waitKey(1) & 0xFF == ord("q"): break
s.close()