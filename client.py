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
    connected = True
    while connected:
        try:
            msg = client.recv(SIZE).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            print("New message: ", msg)
            Messages.append(msg)
        except:
            client.close()
            break

def write(client):
    while True:
        msg = input("> ")
        if msg == DISCONNECT_MSG:
            client.close()
            break
        client.send(msg.encode(FORMAT))
           
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(F"[CONNECTED] Client is connected to {IP}:{PORT}")
    recieve = threading.Thread(target = recieveMsg, args=(client,))
    writes = threading.Thread(target= write,args=(client,))
    recieve.start()
    writes.start()

if __name__ == '__main__':
    main()