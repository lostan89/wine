from http.server import HTTPServer, SimpleHTTPRequestHandler


server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
server.serve_forever()