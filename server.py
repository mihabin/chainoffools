import ssl

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

httpd = HTTPServer(("localhost", 4443), BaseHTTPRequestHandler)

httpd.socket = ssl.wrap_socket(httpd.socket, keyfile="cert.key", certfile="cert_chain.crt", server_side=True)

httpd.serve_forever()
