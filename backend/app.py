from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            response = {
                "remote_addr": self.client_address[0],
                "x_forwarded_for": self.headers.get("X-Forwarded-For"),
                "x_real_ip": self.headers.get("X-Real-IP"),
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps(response, indent=2).encode()
            )

        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")


server = HTTPServer(("0.0.0.0", 8080), Handler)
server.serve_forever()






















# from http.server import BaseHTTPRequestHandler, HTTPServer

# class Handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == "/":
#             self.send_response(200)
#             self.end_headers()
#             self.wfile.write(b"Hello from Effective Mobile!")
#         elif self.path == "/health":
#             self.send_response(200)
#             self.end_headers()
#             self.wfile.write(b"OK")

# server = HTTPServer(("0.0.0.0", 8080), Handler)
# server.serve_forever()






