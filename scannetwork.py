from scapy.all import ICMP, IP, sr1, conf
import socket
import threading

def ping(ip):
    packet = IP(dst=ip)/ICMP()
    response = sr1(packet, timeout=1, verbose=0)
    if response:
        return ip

def check_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return ip

def scan_network(network, port):
    ip_range = network.split('.')
    base_ip = f"{ip_range[0]}.{ip_range[1]}.{ip_range[2]}."
    available_ips = []

    threads = []
    for i in range(1, 255):
        ip = base_ip + str(i)
        thread = threading.Thread(target=lambda q, arg1: q.append(ping(arg1)), args=(available_ips, ip))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    active_ips = [ip for ip in available_ips if ip]

    communicating_ips = []
    threads = []
    for ip in active_ips:
        thread = threading.Thread(target=lambda q, arg1: q.append(check_port(arg1, port)), args=(communicating_ips, ip))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return [ip for ip in communicating_ips if ip]

def connect_to_ip(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip, port))
            print(f"Připojeno k {ip}:{port}")
            send_thread = threading.Thread(target=send_messages, args=(sock,))
            receive_thread = threading.Thread(target=receive_messages, args=(sock,))
            
            send_thread.start()
            receive_thread.start()
            
            send_thread.join()
            receive_thread.join()
        except Exception as e:
            print(f"Nelze se připojit k {ip}:{port} - {e}")

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(f"Zpráva: {message}")
            else:
                break
        except:
            break

def send_messages(sock):
    while True:
        message = input("")
        sock.sendall(message.encode())
        if message.lower() == 'exit':
            break

if __name__ == "__main__":
    network = input("Zadejte síťový rozsah (např. 192.168.1.0): ")
    port = 12345
    print(f"Vyhledávání dostupných IPv4 adres na portu {port}...")
    communicating_ips = scan_network(network, port)
    print("Dostupné IP adresy pro komunikaci na portu 12345:")
    for ip in communicating_ips:
        print(ip)
        connect_to_ip(ip, port)
