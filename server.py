# pylint: disable=line-too-long
"""
server module is a simple server that uses the forged certificate
"""
import ssl

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

HTTPD = HTTPServer(("localhost", 4443), BaseHTTPRequestHandler)

HTTPD.socket = ssl.wrap_socket(HTTPD.socket, keyfile="cert.key", certfile="cert_chain.crt", server_side=True)

HTTPD.serve_forever()
