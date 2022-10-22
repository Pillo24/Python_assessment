# Imagine you have a long running query to obtain in code token.
# How you would use threads to reduce the running time from 5 seconds to 1 second or less?
# You must make a request to server and per response, the response needs to be parsed from json
# All responses need to be saved into request_responses List
# Modify Assesment class as needed

import threading, requests
import time
from server import Server
import asyncio

from multiprocessing.pool import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# A comment added


class Assesment:
    request_responses = []
    server_address = "http://127.0.0.1:8000"

    # async def main(self):        
    #     loop = asyncio.get_running_loop() 
    #     async with ProcessPoolExecutor() as pool:
    #         result = await loop.run_in_executor(pool, self.make_request)
    #         print('custom process pool', result)

    
    
    def start(self):
        elapsed_time = time.time()
        
        #1. Using Traditional Threading technique 
        make_request_thread_list = []
        for i in range(0, 5):        
            # self.make_request()
            # calling make request using thread
            make_request_thread = threading.Thread(target=self.make_request)
            make_request_thread_list.append(make_request_thread)
            make_request_thread.start()
        
        for i in range(0, 5):
            make_request_thread_list[i].join()
        ######################################
        
        #2. Using multiprocessing
        # with Pool() as pool:
        #     pool.starmap(self.make_request,[() for _ in range(5)])
        
        #3. using threadpoolexecutor
        # with ThreadPoolExecutor() as executor:
        #     executor.map(self.make_request,[])
        #     executor.shutdown(wait=True)
            
        # with ThreadPoolExecutor(max_workers=(5)) as executor:
        #     [executor.submit(self.make_request) for _ in  range(5)]
            
            
        # 4. Asyncio Method    
        # asyncio.run(self.main())

            
        self.validate_responses()
        print("Elapsed time: {:.6f}s".format(time.time() - elapsed_time))

    
        
    

    def validate_responses(self):
        if (len(self.request_responses) == 5):
            print("Success")
        else:
            print("Fail")
        print(self.request_responses)

    def make_request(self):
        # pass
        response = requests.get(self.server_address)
        self.request_responses.append(response.json()['success'])


if __name__ == '__main__':
    server = Server()
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    assesment = Assesment()
    try:
        assesment.start()
    except Exception as error:
        print(error)
    finally:        
        server.shutdown()
        server_thread.join()
        server.server_close()
    while server.running:
        print("in while")
        pass
    


    

