import socket
import random

def dh_key_exchange(q, alpha, yb):
    xa = random.randint(1, q - 1)
    ya = pow(alpha, xa, q)
    key = pow(yb, xa, q)
    return (key, ya)

def dh_challenge_response(key, r, q):
    g = (r * key) % q
    return g

def main():
    q = 23
    alpha = 5
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(('localhost', 12345))
    socket_server.listen()

    print("Server is listening on localhost:12345")

    client, address = socket_server.accept()
    print(f"Connected to client at {address}")

    key, ya = dh_key_exchange(q, alpha, 0)

    client.sendall(f"{q} {ya}".encode('utf-8'))

    yb = int(client.recv(1024).decode('utf-8'))
    key, _ = dh_key_exchange(q, alpha, yb)

    r = random.randint(1, q - 1)
    client.sendall(f"{r}".encode('utf-8'))

    g = int(client.recv(1024).decode('utf-8'))
    r_prime = (g / key) % q

    if r_prime == r:
        client.sendall("authenticated".encode('utf-8'))
    else:
        client.sendall("non-authenticated".encode('utf-8'))

    client.close()

if __name__ == "__main__":
    main()

