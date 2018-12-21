#!/usr/bin/env python3

import socket

HOST = '192.168.33.10'  # The server's hostname or IP address
PORT = 6001        # The port used by the server

headers = """
POST {route} HTTP/1.1\r
Authorization: Bearer {token}
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
\r\n"""

body = r'{"channel":"private-newgame.4","name":"App\\Events\\GameStarted","data":{"from":"python"},"socket_id":"Z2DqVAmcj1i7a7qrAAAA"}'
body_bytes = body.encode('ascii')
header_bytes = headers.format(
    content_type="application/x-www-form-urlencoded",
    content_length=len(body_bytes),
    host=str(HOST) + ":" + str(PORT),
    token='4e33d408aaeac4b3a93e1b8df0e0fc5c',
    route='/apps/bomberry/events'
).encode('iso-8859-1')

payload = header_bytes + body_bytes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(payload)
    data = s.recv(1024)

print('Received', repr(data))

