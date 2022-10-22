from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from time import sleep

# https://docs.python.org/3/library/socketserver.html#socketserver.ThreadingMixIn
class Server(ThreadingMixIn, HTTPServer):
    server_address = ('127.0.0.1', 8000)
    running = False

    def __init__(self):
        super().__init__(self.server_address, ServerHandler)

    def serve_forever(self, poll_interval: float = ...) -> None:
        print("Server running on {}:{}".format(self.server_address[0], self.server_address[1]))
        self.running = True
        super().serve_forever()

    def server_close(self):
        self.running = False
        super().server_close()


class ServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        sleep(1)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes("{ \"success\": true }", "utf-8"))


