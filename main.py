# Imagine you have a long running query to obtain in code token.
# How you would use threads to reduce the running time from 5
# seconds to 1 second or less?
# You must make a request to server and per response,
# the response needs to be parsed from json
# All responses need to be saved into request_responses List
# Modify Assesment class as needed

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from server import Server


class Assesment:
    request_responses: list = []
    server_address: str = "http://127.0.0.1:8000"
    number_of_requests: int = 5

    def start(self):
        elapsed_time = time.time()

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.make_request_async())
        loop.run_until_complete(future)

        self.validate_responses()
        print("Elapsed time: {:.6f}s".format(time.time() - elapsed_time))

    async def make_request_async(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            with requests.Session() as session:
                loop = asyncio.get_event_loop()

                tasks = [
                    loop.run_in_executor(
                        executor, self.make_request, *(session,)
                    )  # noqa: E731
                    for _ in range(self.number_of_requests)
                ]

                for _ in await asyncio.gather(*tasks):
                    pass

    def validate_responses(self):
        if len(self.request_responses) == self.number_of_requests:
            print("Success")
        else:
            print("Fail")

        print(self.request_responses)

    def make_request(self, session):
        with session.get(self.server_address) as response:
            self.request_responses.append(response.json()["success"])

            if response.status_code != 200:
                print("FAILURE::{}".format(self.server_address))


if __name__ == "__main__":
    server = Server()
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    assesment = Assesment()

    try:
        assesment.start()
    except Exception as error:
        print(error)
    finally:
        print("Cleaning up the server...")
        server.shutdown()
        server.server_close()
        server_thread.join()
