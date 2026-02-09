import socket

# Configuration
IP = "0.0.0.0"  # Listen on all interfaces
PORT = 5005     # Use an open port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))

print(f"Robot Mirror active on port {PORT}. Waiting for PC commands...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        # Immediately reflect the data back to the sender
        sock.sendto(data, addr)
except KeyboardInterrupt:
    print("\nShutting down robot mirror.")
finally:
    sock.close()