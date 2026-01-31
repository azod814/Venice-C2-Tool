import socket
import argparse
from datetime import datetime

def start_listener(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f"🐾 [+] C2 Listener started on {ip}:{port}")
    print(f"🐾 [+] Waiting for a connection...")

    while True:
        client, addr = server.accept()
        print(f"🐾 [+] Connection received from {addr[0]}:{addr[1]} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        data = client.recv(4096)
        if data:
            decoded_data = data.decode('utf-8', errors='ignore')
            print("\n--- RECEIVED DATA ---")
            print(decoded_data)
            print("---------------------\n")
        
        client.close()
        print(f"🐾 [-] Connection from {addr[0]}:{addr[1]} closed.")
        print(f"🐾 [+] Waiting for a new connection...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Venice C2 Listener")
    parser.add_argument("-i", "--ip", required=True, help="Your Kali IP address")
    parser.add_argument("-p", "--port", type=int, default=4444, help="Port to listen on (default: 4444)")
    args = parser.parse_args()
    
    try:
        start_listener(args.ip, args.port)
    except KeyboardInterrupt:
        print("\n🐾 [!] Listener stopped by user.")
    except Exception as e:
        print(f"🐾 [!] An error occurred: {e}")
