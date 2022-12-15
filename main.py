from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from webbrowser import open

open('http://localhost:8000/html')
TCPServer(("", 8000), SimpleHTTPRequestHandler).serve_forever()