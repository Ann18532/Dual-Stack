import socket


def send_file_to_router(router_ip, router_port, filename):
    # Try to resolve both IPv4 and IPv6 addresses
    addr_info = socket.getaddrinfo(
        router_ip, router_port, socket.AF_UNSPEC, socket.SOCK_STREAM
    )

    # Select the first valid address (IPv4 or IPv6)
    for res in addr_info:
        af, socktype, proto, canonname, sa = res
        print(res)
        try:
            client_socket = socket.socket(af, socktype, proto)
            client_socket.connect(sa)
            print(f"Connected to router at {sa}")
            break
        except socket.error:
            client_socket = None
            continue

    if client_socket is None:
        print("Failed to connect to the server.")
        return

    try:
        with open(filename, "rb") as f:
            print(f"Sending '{filename}' to the router...")
            while chunk := f.read(1024):
                client_socket.sendall(chunk)
                print("Sending...")
        print(f"File '{filename}' sent to the router successfully.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred during file transfer: {e}")
    finally:
        client_socket.close()
        print("Connection to router closed.")

    print(f"File '{filename}' sent successfully.")

    # Close the socket
    client_socket.close()


router_ip = "127.0.0.1"
router_port = 12346
filename = "msg.txt"
send_file_to_router(router_ip, router_port, filename)
#test here and write the params to the test.txt






