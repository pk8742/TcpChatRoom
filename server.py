import threading
import socket

host = '127.0.0.1'  # localhost
port = 55555
# creating server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding server
server.bind((host, port))
server.listen()  # putting server in listening mode

clients = []
nicknames = []
# method to broadcast each received message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# handling clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:  # cut the connection, remove client and terminate method
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat !".encode('ascii'))
            break

# defining main method, receives client connection
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")
        # get nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of client is: {nickname}")
        broadcast(f"{nickname} join the chat".encode('ascii'))
        client.send("connected to server".encode('ascii'))
        # handling multiple clients
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Initializing
print("Server is listening")
receive()
