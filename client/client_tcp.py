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
        print_progress_bar()  # Llama a la función para imprimir la barra de progreso
        print(colored("\n[] Hosts encontrados: ", "green") + str(hosts))

        with open('hosts.json', 'w') as file:
            json.dump(hosts, file)

        return hosts

def ping_hosts():
    global server_ip
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


def tcp_bind():
    try:
        print(colored("[+] Creating socket...", "blue"))
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(colored("[-] Error creating socket: " + str(e), "red"))
        sys.exit()
    return tcp_sock

def connect_to_server():
    client = tcp_bind()
    client.connect((server_ip, 8080))
    print(colored("[+] Connected to server!", "green"))
    while True:
        msg = input(colored("Msg: ", "blue"))
        
        try:
            client.sendall(msg.encode())
            
            reply = client.recv(1024)
            print(colored("[] Server reply: " + reply.decode(), "green"))
        except socket.error as e:
            print(colored("[-] Error sending data: " + str(e), "red"))
            sys.exit()


if __name__ == '__main__':
    
    while True:
        response = input("Do you want to skip the network scan and enter the server's IP manually? [y/n]: ").lower()
        if response in ['y', 'yes']:
            server_ip = input(colored("[?] Please, introduce the server's IP", "blue"))
            connect_to_server()
            break
        elif response in ['n', 'no']:
            ping_hosts()
            if server_ip == None:
                server_ip = input(colored("[?] Please, manually introduce the server's IP", "blue"))
            connect_to_server()
            break
        else:
            print("Please enter a valid option: y/yes or n/no")
    
    
    
    
    
