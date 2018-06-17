import http.server
import socketserver
import ssl

httpd = socketserver.TCPServer(('localhost', 4443), http.server.SimpleHTTPRequestHandler)

httpd.serve_forever()