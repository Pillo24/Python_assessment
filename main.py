# Imagine you have a long running query to obtain in code token.
# How you would use threads to reduce the running time from 5 seconds to 1 second or less?
# You must make a request to server and per response, the response needs to be parsed from json
# All responses need to be saved into request_responses List
# Modify Assesment class as needed

import threading
import time
import requests
import concurrent.futures
from server import Server, ServerHandler

class Assesment:
    server_address = "http://127.0.0.1:8000"

    def __init__(self):
        #threading.Thread.__init__(self)
        self.request_responses = [] #reqest_responses is more like an instance attribute than lile a class one

    def start(self):
        elapsed_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            jobs = {executor.submit(self.make_request, self.server_address): self.server_address for i in range(0, 5)}
        for future in concurrent.futures.as_completed(jobs):
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (self.server_address, exc))
            else:
                self.request_responses.append(data)
        self.validate_responses()
        print("Elapsed time: {:.6f}s".format(time.time() - elapsed_time))

    def validate_responses(self):
        if (len(self.request_responses) == 5):
            for response in self.request_responses:
                assert response["success"]
                assert response["request_num"] <= 5
                assert response["final_request_num"] <= 5
            print("Success")
        else:
            print("Fail")
        #print(self.request_responses)

    def make_request(self, address):
        request_response = requests.get(address)
        request_json = request_response.json()
        return request_json


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
