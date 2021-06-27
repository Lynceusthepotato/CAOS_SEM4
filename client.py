import tkinter as tk
from tkinter import messagebox
import socket
import threading

# Server config
SIZE = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
IP = socket.gethostbyname("localhost")
ADDR = (IP, PORT)
    
clientNickname = input("Type in your nickname! > ")
Messages = []

def recieveMsg(client):
    connected = True
    while connected:
        try:
            msg = client.recv(SIZE).decode(FORMAT)
            if msg == 'NICK':
                client.send(clientNickname.encode(FORMAT))
            elif msg == DISCONNECT_MESSAGE:
                connected = False
            print(msg)
        except:
            client.close()
            break

def write(client):
    while True:
        # msg = f'{clientNickname}: {input("")}'
        msg = input("> ")
        # print (msg)
        if msg == DISCONNECT_MESSAGE:
            client.close()
            break
        client.send(msg.encode(FORMAT))
           
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    # print(F"[CONNECTED] Client is connected to {IP}:{PORT}")
    recieve = threading.Thread(target = recieveMsg, args=(client,))
    writes = threading.Thread(target= write,args=(client,))
    recieve.start()
    writes.start()

if __name__ == '__main__':
    main()