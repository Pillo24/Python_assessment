# Imagine you have a long running query to obtain in code token.
# How you would use threads to reduce the running time from 5 seconds to 1 second or less?
# You must make a request to server and per response, the response needs to be parsed from json
# All responses need to be saved into request_responses List
# Modify Assesment class as needed

import requests
from server import Server
import threading
import time


class Assesment:
    request_responses = []
    server_address = "http://127.0.0.1:8000"

    def start(self):
        elapsed_time = time.time()
        threads = []
        for i in range(0, 5):
            threads.append(threading.Thread(target=self.make_request))
        self.thread_start(threads)
        self.thread_join(threads)
        self.validate_responses()
        print("Elapsed time: {:.6f}s".format(time.time() - elapsed_time))

    def validate_responses(self):
        if (len(self.request_responses) == 5):
            print("Success")
        else:
            print("Fail")
        print(self.request_responses)

    def make_request(self):
        request_response = requests.get(self.server_address)
        response_json = request_response.json()
        self.request_responses.append(response_json)

    def thread_start(self, threads):
        for thread in threads:
            thread.start()

    def thread_join(self, threads):
        for thread in threads:
            thread.join()


if __name__ == '__main__':
    server = Server()
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    assesment = Assesment()
    try:
        assesment.start()
    except Exception as error:
        print(error)
    while server.running:
        pass
