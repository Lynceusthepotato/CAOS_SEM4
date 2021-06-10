import socket
import threading

IP = socket.gethostbyname("localhost")
PORT = 5050
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!BYE"

clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    try:
        while connected:
            msg = conn.recv(SIZE).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                clients.remove(conn)
                connected = False
            elif not msg:
                clients.remove(conn)
                connected = False
            broadcast(msg)
    except ConnectionResetError as e:
        print("SOMEONE Disconnected")
        clients.remove(conn)
        
def send(s, msg):
    s.send(msg.encode(FORMAT))

def broadcast(msg):
    for c in clients:
        send(c, msg)

def main():
    print(f"[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    
    while True:
        # Limit the user to only 2 since playing rps
        # For now its only for communication
        if threading.activeCount() <= 2:
            conn, addr = server.accept()
            clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[CONNECTIONS] {threading.activeCount() - 1}")
        else:
            server.close()

if __name__ == "__main__":
    main()