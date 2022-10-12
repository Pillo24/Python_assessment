from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from time import sleep
import json
import concurrent.futures

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

    request_num = 0
    def do_GET(self) -> None:
        ServerHandler.request_num += 1
        dct = {"success": True, "request_num": ServerHandler.request_num}
        # The second to be waited is divided in 2 hemiseconds, that each one is waited in a
        # separate thread, almost simultaneously
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            jobs = {executor.submit(self.wait_half_second): i for i in range(0, 2)}
        for future in concurrent.futures.as_completed(jobs):
            try:
                data = future.result()
            except Exception as exc:
                print('The Future object generated an exception: %s' % (exc))
            assert data == 'waited 0.5 seconds'
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        dct["final_request_num"] = ServerHandler.request_num
        #Most probably all the 'final_request_num' values will be 5, because multiple threads will have
        # accessed the class object to increase the erverHandler.request_num variable by 1
        print("this request will return:", dct)
        self.wfile.write(bytes(json.dumps(dct), "utf-8"))

    def wait_half_second(self):
        sleep(0.5)
        return 'waited 0.5 seconds'


