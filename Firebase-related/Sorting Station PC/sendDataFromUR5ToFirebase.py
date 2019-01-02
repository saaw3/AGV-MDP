# server
# message receiver

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import socket

# initialise socket to listen to UR5 from PC
fireBaseSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fireBaseSocket.bind((socket.gethostname(), 13000))
fireBaseSocket.listen(5)
print("fireBaseSocket listening")
UR5, address = fireBaseSocket.accept()
print("Got connection from ", address)

# initialise connection to Firebase
cred = credentials.Certificate('C:\\Users\\EEE\\Desktop\\jsonKeyFileFirebase.json')
firebase_admin.initialize_app(cred)

dataBase = firestore.client()
print("Connected to Google Firebase")
UR5Position = dataBase.collection(u'UR5').document(u'position')

while True:
    # accept and receive data from UR5
    data = UR5.recv(1024)
    print("Data received is " + data)

    # update Google Firebase with position
    if data == "moveLeft":
        UR5Position.update({
            u'direction': u'Left',
        })
    elif data == "moveRight":
        UR5Position.update({
            u'direction': u'Right',
        })
    elif not data:
        break

UR5.close()
