import socket
import threading

scores = sorted([("Chris", 60), ("Alex", 40), ("Elon Musk", 400)], key=lambda tup:tup[1], reverse=True)
port = 4269
host = "localhost"


def handle(client_sock):
    recvthread = threading.Thread(target=handlerecv, args=(client_sock,))
    recvthread.start()

def handlerecv(client_sock):
    try:
        while True:
            global scores
            new_score = client_sock.recv(1024).decode().split("\n")
            print(new_score)
            new_score_tuple = (new_score[1], int(new_score[0]))
            print(new_score_tuple)
            scores.append(new_score_tuple)
            scores.sort(key=lambda tup:tup[1], reverse=True)
            client_sock.send(str(scores).encode())
    except ConnectionAbortedError:
        print("Client has closed connection")


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))

    server_sock.listen()

    print("Server is listening")
    while True:
        (client_sock, addr) = server_sock.accept()
        # blocking method
        thread = threading.Thread(target=handle, args=(client_sock,))
        thread.start()


main()