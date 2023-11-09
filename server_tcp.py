import socket
from termcolor import colored
import sys
import select

host = ''
port = 8080
colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
clients = {}

def eco_udp():
    try:
        print(colored("[+] Creating socket...", "blue"))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(colored("[] Socket succsesfully created!", "green"))
    except socket.error as e:
        print(colored("[-] Error creating socket: " + str(e), "red"))
    try:
        print(colored("[+] Binding socket...", "blue"))
        s.bind(('', 8080))
        s.settimeout(15)
        print(colored("[] Socket binded successfully!", "green"))
    except socket.error as e:
        print(colored("[-] Error binding socket: " + str(e), "red"))
    try:    
        print(colored("[+] Listening...", "blue"))
        msg, (addr, port) = s.recvfrom(1024)
        print(colored("[] Ping received from " + addr, "green"))
        s.sendto(b'pong', (addr, port))
        if msg.decode().strip() == 'ping':
            s.sendto(b'pong', (addr, port))
            s.close()
    except socket.timeout:
        print(colored("[-] Timeout waiting for ping response, exiting...", "red"))

def set_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen(10)
    print(colored("[] Server listening on port " + str(port), "green"))
    return server


if __name__ == "__main__":
    eco_udp()
    print(colored("[?] Assuming that the port is 8080", "blue"))
    server_port = 8080
    server = set_server(server_port)
    descriptors = [server]
    while True:
        (sread, swrite, sexc) = select.select(descriptors, [], [])
        
        for sock in sread:
            if sock == server:
                conn, addr = server.accept()
                print(colored("[] Connection from " + str(addr[0]) + " on port " + str(addr[1]), "green"))
                descriptors.append(conn)
                clients[conn] = addr
            else:
                data = sock.recv(1024)
                
                if not data:
                    host, port = clients[sock]
                    print(colored("[-] Connection closed by " + str(host) + " on port " + str(port), "red"))
                    sock.close()
                    descriptors.remove(sock)
                    del clients[sock]
                else:
                    host, port = clients[sock]
                    print(colored("[] Received " + str(data.decode().strip()) + " from " + str(host) + " on port " + str(port), "green"))
                    
                    for client_socket in clients:
                        if client_socket != server and client_socket != sock:
                            try:
                                client_socket.sendall(data)
                            except socket.error:
                                host, port = clients[client_socket]
                                print(colored("[-] Connection closed by " + str(host) + " on port " + str(port), "red"))
                                client_socket.close()
                                descriptors.remove(client_socket)
                                del clients[client_socket]
    server.close()
