import socket
import sys
import select


def client():
    # establish socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if len(sys.argv) != 3:
        print("Please enter: scriptname, IP address, port number")

    IP = str(input("IP server: "))
    port = int(input("PORT server: "))

    name = str(input("Please enter your name: "))

    # connect to server
    try:
        server_sock.connect((IP, port))
        print("Trying to connect...")
    except:
        print("Can't connect to server")
        sys.exit()

    server_sock.send(name.encode("utf8"))
    connected = True
    data = server_sock.recv(2048).decode("utf8")  # welcome message
    print("<" + IP + ">: " + data)
    while connected:
        socket_list = [sys.stdin, server_sock]
        try:

            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
            for sock in read_sockets:
                if sock == server_sock:
                    data = server_sock.recv(2048).decode("utf8")  # чужие сообщения
                    if len(data) == 0:
                        print("You have disconnected.")
                        sys.exit()
                else:
                    my_msg = sys.stdin.readline()  # мои сообщения
                    server_sock.send(my_msg.encode("utf8"))
        except:
            print("You have disconnected manually")
            connected = False

    print("You have disconnected ")


if __name__ == '__main__':
    client()

# TODO: Print list of current users to client
