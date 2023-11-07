import socket
from termcolor import colored
import sys
import threading
import random

host = ''
port = 8080
colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

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
    except socket.timeout:
        print(colored("[-] Timeout waiting for ping response, exiting...", "red"))
        sys.exit()

    if msg.decode().strip() == 'ping':
        s.sendto(b'pong', (addr, port))
        s.close()

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break

            if client_address[0] not in color_mapping:
                color = random.choice(colors)
                color_mapping[client_address[0]] = color
                colors.remove(color)

            formatted_message = f"[{colored(client_address[0], color_mapping[client_address[0]])}]: {message}"
            print(formatted_message)

            # Enviar el mensaje a todos los clientes
            for address, socket in client_sockets.items():
                if address != client_address:
                    sender_ip = f"[{colored(client_address[0], color_mapping[client_address[0]])}]"
                    message_to_send = f"{sender_ip}: {message}"
                    socket.send(message_to_send.encode("utf-8"))

        except ConnectionResetError:
            break

    client_socket.close()
    del client_sockets[client_address]

def start_server():
    host = ''
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(25)

    print(colored(f"[*] Listening as {host}:{port}", "blue"))

    while True:
        client_socket, client_address = server_socket.accept()
        client_sockets[client_address] = client_socket

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    eco_udp()
    color_mapping = {}
    client_sockets = {}
    start_server()
