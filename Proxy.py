# Charbel Toumieh
# ID: 202218744

import socket
import time

host = '127.7.77.77'
port = 7787  # The port for the proxy server.
# Acceptable port from 0 to 65535, taken from https://www.ibm.com/docs/en/rtw/9.1.0?topic=setup-modifying-configuration-settings-httptcp-proxy

# TCP socket to listen for incoming connections.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # TCP taken from code on MOODLE
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # This is to reuse the same port if it is already in use
    # Sometimes when running it multiple times, the port can still be in use, so this reuses the same port removing that problem
    # Learned about it through https://www.programcreek.com/python/example/410/socket.SO_REUSEADDR
    
    s.bind((host, port))  # Here we bind the socket to the host and port.
    s.listen(1)  # And we start listening for incoming connections.
    print("Listening on " + str(host) + ":" + str(port))  # Print a message to the console.

    while True:
        conn, addr = s.accept()  # Accepts a new incoming connection.
        print("Accepted connection from " + str(addr) + " at " + str(time.ctime()))  # Show acceptance of connection

        request = conn.recv(4096).decode()  # Receive the client's request.
        if not request:  # If the request is empty, send an error message to the client and close the connection.
            print("Error: Empty request from " + addr + " at " + time.ctime())
            conn.sendall("HTTP/1.1 400 Bad Request\n\n")
            conn.close()
            continue

        lines = request.split("\r\n")  # Split the request into lines.
        method, path, _ = lines[0].split()  # Get the method and path from the first line.
        host_header = [line for line in lines if line.startswith("Host:")]  # Get the host header from the request.
        if not host_header:  # If host header is missing, send an error message to the client and close the connection.
            print("Error: No host header in request from " + str(addr) + " at " + str(time.ctime()))
            conn.sendall("HTTP/1.1 400 Bad Request\n\n".encode('utf-8'))
            conn.close()
            continue
            
        host, _, port = host_header[0].split()[1].partition(":")  # Parse host header, get destination server IP + port
        port = int(port) if port else 80  # If the port is missing, use port 80.
        ip = socket.gethostbyname(host)  # Gets IP from URL
        # To get the IP from URL was taken from https://www.digitalocean.com/community/tutorials/python-get-ip-address-from-hostname

        print(str(host_header) + " [IP: " + str(host) + " is " + str(ip) + "]")

        print("Forwarding request to " + host + ":" + str(port) + " at " + time.ctime())

        # Send the client's request to the destination server.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as dest_sock:
            dest_sock.settimeout(10)  # 10 seconds timeout in case the destination server is unavailable (tried with 5 seconds, in some cases timeout passed).
            
            try:
                dest_sock.connect((host, port))  # Connect to the destination server.
                dest_sock.sendall(request.encode())  # Send the request to the destination server.
            except socket.timeout:
                print("Error: Connection timed out to " + host + ":" + str(port) + " at " + time.ctime())
                conn.sendall("HTTP/1.1 504 Gateway Timeout\n\n")
                conn.close()
                continue
                
            except socket.error as e:
                print("Error: Connection to " + str(host) + ":" + str(port) + " failed with " + str(e) + " at " + time.ctime())
                conn.sendall("HTTP/1.1 504 Gateway Timeout\n\n")
                conn.close()
                continue

            print("Request sent to " + str(host) + ":" + str(port) + " at " + time.ctime())

            response = dest_sock.recv(4096)  # Receive the response from the destination server.
            if not response:  # If the response is empty, send an error message to the client and close the connection.
                print("Error: Empty response from " + host + ":" + str(port) + " at " + time.ctime())
                conn.sendall("HTTP/1.1 504 Gateway Timeout\n\n")
                conn.close()
                continue
                
        print("Response received from " + host + ":" + str(port) + " at " + time.ctime())

        conn.sendall(response)  # Send the response back to the client.
        print("Response sent to " + str(addr) + " at " + str(time.ctime()))

        conn.close()  # Close the connection to the client.
