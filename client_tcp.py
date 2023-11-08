
import socket
import sys
from termcolor import colored
import nmap
import json
import os
import time
import threading

server_ip = None

def print_progress_bar():
    BAR_LEN=30
    elements = ['\\', '|', '/', '-']
    for i in range(BAR_LEN):
        frame = i % len(elements)
        print(f'\r[{elements[frame]*i:=<{BAR_LEN}}]', end='')
        time.sleep(0.1)

def find_hosts():
    if os.path.exists('hosts.json'):  # Comprueba si el archivo hosts.json existe
        with open('hosts.json', 'r') as file:
            hosts = json.load(file)
        print(colored("[] Hosts encontrados: ", "green") + str(hosts))
        return hosts
    else:
        print(colored("[+] Archivo hosts.json no encontrado.", "yellow"))
        range_input = input("Ingresa el rango de red (por ejemplo, 192.168.1.0/24): ")
        nm = nmap.PortScanner()
        print(colored("[+] Escaneando red...", "yellow"))
        nm.scan(hosts=range_input, arguments='-n -sP')
        hosts = nm.all_hosts()
        hosts.append('192.168.99.34')
        print_progress_bar()  # Llama a la función para imprimir la barra de progreso
        print(colored("\n[] Hosts encontrados: ", "green") + str(hosts))

        with open('hosts.json', 'w') as file:
            json.dump(hosts, file)

        return hosts

def ping_hosts():
    try:
        print(colored("[+] Creating socket...", "blue"))
        ping_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ping_sock.settimeout(1)
        print(colored("[] Socket succsesfully created!", "green"))
        found_hosts = find_hosts()
    except socket.error as e:
        print(colored("[-] Error creating socket: " + str(e), "red"))
        sys.exit()

    for host in found_hosts:
        print(colored("\n[+] Sending pings!", "blue"))
        ping_sock.sendto(b'ping', (host, 8080))
        
        print(colored("[+] Ping sent to " + host, "green"))
        try:
            msg, (addr, port) = ping_sock.recvfrom(1024)
            if msg.decode().strip() == 'pong':
                print(colored("\n[+] Pong received from " + addr + " from port " + str(port), "green"))
                server_ip = addr
        except socket.timeout:
            print(colored("[-] Timeout waiting for ping response from " + host, "red"))
    ping_sock.close()
    try:
        return server_ip
    except UnboundLocalError as e:
        print(colored("[-] No se encontró el servidor, intenta de nuevo.", "red"))
        print(colored("[-] Error: " + str(e), "red"))
        sys.exit()

def tcp_bind():
    try:
        print(colored("[+] Creating socket...", "blue"))
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(colored("[-] Error creating socket: " + str(e), "red"))
        sys.exit()
    try:
        print(colored("[+] Binding socket...", "blue"))
        tcp_sock.bind(('', 8080))
        tcp_sock.settimeout(5)
        print(colored("[] Socket binded successfully!", "green"))
    except socket.error as e:
        print(colored("[-] Error binding socket: " + str(e), "red"))
        sys.exit()
    try:
        print(colored("[+] Listening...", "blue"))
        tcp_sock.listen(1)
        print(colored("[] Socket listening successfully!", "green"))
    except socket.error as e:
        print(colored("[-] Error listening socket: " + str(e), "red"))
        sys.exit()
    try:
        print(colored("[+] Accepting connections...", "blue"))
        conn, addr = tcp_sock.accept()
        print(colored("[] Connection accepted from " + addr[0], "green"))
    except socket.error as e:
        print(colored("[-] Error accepting connection: " + str(e), "red"))
        sys.exit()
        
def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode("utf-8")
        print(message)

def start_client(server_ip):
    host = server_ip
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Mensaje: ")

        formatted_message = f"[{colored(socket.gethostbyname(socket.gethostname()), 'green')}]: {message}"
        client_socket.send(formatted_message.encode("utf-8"))        

if __name__ == '__main__':
        server_ip=ping_hosts()
        start_client(server_ip)
    