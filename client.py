import socket
import random

def dh_key_exchange(q, alpha, ya):
    xb = random.randint(1, q - 1)
    yb = pow(alpha, xb, q)
    key = pow(ya, xb, q)
    return (key, yb)

def dh_challenge_response(key, r, q):
    g = (r * key) % q
    return g

def main():
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(('localhost', 12345))

    q, ya = map(int, socket_client.recv(1024).decode('utf-8').split())
    key, yb = dh_key_exchange(q, alpha, ya)
    socket_client.sendall(f"{yb}".encode('utf-8'))

    r = int(socket_client.recv(1024).decode('utf-8'))
    g = dh_challenge_response(key, r, q)
    socket_client.sendall(f"{g}".encode('utf-8'))

    result = socket_client.recv(1024).decode('utf-8')
    print(f"Result from server: {result}")
    socket_client.close()

if __name__ == "__main__":
    main()
