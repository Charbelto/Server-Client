# Charbel Toumieh
# ID: 202218744

import socket
import time
import uuid

website_host = input("Please enter an website URL or an IP address:")  # website url/ip
website_port = 80  # website port
# Used port 80 with help from http://www.steves-internet-guide.com/tcpip-ports-sockets/

proxy_host = "127.7.77.77"  # ip of proxy server
proxy_port = 7787  # port for proxy server, here I chose 7787

# Create a socket for connecting to the proxy server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  # TCP taken from code on MOODLE
    client_socket.connect((proxy_host, proxy_port))  # connection to proxy server

    # Construct the request to send to the website
    request = (
            "GET / HTTP/1.1\r\n"
            "Host: " + website_host + ":" + str(website_port) + "\r\n"  # convert website_port to string
            "\r\n"
    )

    start_time = time.time()  # records start time before sending the request

    client_socket.sendall(request.encode())  # sends request to proxy server
    # prints start time
    print("Request sent to " + str(proxy_host) + ":" + str(proxy_port) + " at " + str(time.ctime(start_time)))
    print("Request asking for " + website_host + " on port " + str(website_port))
    response = client_socket.recv(4096).decode()  # receives response from proxy server

    end_time = time.time()  # records end time after receiving the response

    # prints end time
    print("Response received from " + str(proxy_host) + ":" + str(proxy_port) + " at " + str(time.ctime(end_time)))
    print("Response:")
    print(response)  # prints response

    round_trip_time = end_time - start_time  # calculates total round trip time
    print("Round-trip time:" + str(round_trip_time) + " seconds")  # prints round trip time

    mac = uuid.getnode()  # gets mac address
    print("MAC address:" + str(mac))  # prints mac address
