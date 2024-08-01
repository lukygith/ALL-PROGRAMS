# client.py
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(message.decode("utf-8"))
            else:
                break
        except:
            print("Connection closed")
            client_socket.close()
            break

def main():
    primary_server_ip = "192.168.1.48"
    primary_server_port = 12345

    primary_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    primary_client.connect((primary_server_ip, primary_server_port))
    print("Connected to the primary server")

    mode = input("Do you want to create a new port or use an existing port? (new/existing): ").strip().lower()
    if mode == "new":
        primary_client.send("new".encode("utf-8"))
        response = primary_client.recv(1024).decode("utf-8")
        if response.startswith("new_port:"):
            server_port = int(response.split(":")[1])
            print(f"New port assigned: {server_port}")
    elif mode == "existing":
        server_port = int(input("Enter the existing port number: "))
        primary_client.send(f"existing:{server_port}".encode("utf-8"))
        response = primary_client.recv(1024).decode("utf-8")
        if response == "port_unavailable":
            print("The port is not available. Please try again.")
            return
    else:
        print("Invalid option")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((primary_server_ip, server_port))
    print(f"Connected to the server on port {server_port}")

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == "exit":
            client.close()
            break
        client.send(message.encode("utf-8"))

if __name__ == "__main__":
    main()
