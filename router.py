import socket
import threading
import signal
import sys

running = True

def signal_handler(sig, frame):
    global running
    running = False

def handle_client(client_socket, server_address, server_port):
    """Handles forwarding data from client to server."""
    try:
        # Create a connection to the server
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((server_address, server_port))
            print(f"Connected to server at {server_address}:{server_port}")
            
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # Forward the data to the server
                server_socket.sendall(data)
                
            print("File relayed to server.")
    except Exception as e:
        print(f"Error relaying data to the server: {e}")
    finally:
        client_socket.close()

def start_router(router_host_ipv4, router_port_ipv4, router_host_ipv6, router_port_ipv6, server_address, server_port):
    """Starts the router to relay traffic between clients and server."""
    # Create a socket for IPv4
    ipv4_router_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipv4_router_socket.bind((router_host_ipv4, router_port_ipv4))
    ipv4_router_socket.listen(5)
    print(f"IPv4 Router listening on {router_host_ipv4} port {router_port_ipv4}")

    # Create a socket for IPv6
    ipv6_router_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    ipv6_router_socket.bind((router_host_ipv6, router_port_ipv6))
    ipv6_router_socket.listen(1)
    print(f"IPv6 Router listening on {router_host_ipv6} port {router_port_ipv6}")

    while running:
        client_socket_ipv4, addr_ipv4 = ipv4_router_socket.accept()
        print(f"IPv4 connection from {addr_ipv4}")

        client_thread_ipv4 = threading.Thread(
            target=handle_client, 
            args=(client_socket_ipv4, server_address, server_port)
        )
        client_thread_ipv4.start()

        client_socket_ipv6, addr_ipv6 = ipv6_router_socket.accept()
        print(f"IPv6 connection from {addr_ipv6}")

        client_thread_ipv6 = threading.Thread(
            target=handle_client, 
            args=(client_socket_ipv6, server_address, server_port)
        )
        client_thread_ipv6.start()

    ipv4_router_socket.close()
    ipv6_router_socket.close()
    print("Router closed successfully.")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler) 
    start_router('127.0.0.1', 12346, '::1', 12347, '::1', 12345)  
    # IPv4 router listens on port 12346 and IPv6 router listens on port 12347


