import socket
import threading
import os

IP = socket.gethostbyname("localhost")
PORT = 5050
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!BYE"

Messages = []

def recieveMsg(client):
    while True:
        msg = client.recv(SIZE).decode(FORMAT)
        print("New message: ", msg)
        Messages.append(msg)
            
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(F"[CONNECTED] Client is connected to {IP}:{PORT}")
    recieve = threading.Thread(target = recieveMsg, args=(client,))
    recieve.start()
    
    connected = True
    while connected:
        msg = input("> ")
        
        client.send(msg.encode(FORMAT))
        
        if msg == DISCONNECT_MSG:
            connected = False

if __name__ == '__main__':
    main()