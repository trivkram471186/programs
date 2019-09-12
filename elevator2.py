import threading
import time

from enum import Enum

class direction(Enum):
        NONE = 0
        UPWARD = 1
        DOWNWARD = 2
        
class lift:
        def __init__(self):
            self.current_floor = 0
            self.moving = False
            self.requests = []
            self.current_request = 0
            self.direction = direction.NONE

l1 = lift()
l2 = lift()

list_of_requests = []

def run(lock):
    while True:
        i = input()
       
        list_of_requests.append(i)

        print("list of requests = {}".format(list_of_requests))
       
def run2(lock):
        while True:
                while len(l1.requests) == 0:
                        pass


                l1.current_request = l1.requests.pop()
                if l1.current_floor < l1.current_request:
                        while l1.current_floor != l1.current_request:
                                time.sleep(1)
                                l1.current_floor = l1.current_floor + 1

                                # handle intermediate requests
                                if l1.current_floor in l1.requests:
                                        print("lift 1 stopped at floor {}".format(l1.current_floor))
                                        l1.requests.remove(l1.current_floor)
                                        time.sleep(5)
                                else:
                                        print("lift 1 moving, current_floor: {}".format(l1.current_floor))
                        print("lift 1: current_floor: {}".format(l1.current_floor))
                else:
                        while l1.current_floor != l1.current_request:
                                time.sleep(1)
                                l1.current_floor = l1.current_floor - 1

                                # handle intermediate requests
                                if l1.current_floor in l1.requests:
                                        print("lift 1 stopped at floor {}".format(l1.current_floor))
                                        l1.requests.remove(l1.current_floor)
                                        time.sleep(10)
                                else:
                                        print("lift 1 moving, current_floor: {}".format(l1.current_floor))
                                
                        print("lift 1: current_floor: {}".format(l1.current_floor))


def run3(lock):
        while True:
                while len(l2.requests) == 0:
                        pass

                l2.current_request = l2.requests.pop()
                if l2.current_floor < l2.current_request:
                        while l2.current_floor != l2.current_request:
                            time.sleep(1)
                            l2.current_floor = l2.current_floor + 1

                            # handle intermediate requests
                            if l2.current_floor in l2.requests:
                                    print("lift 2 stopped, current_floor: {}".format(l2.current_floor))
                                    l2.requests.remove(l2.current_floor)
                                    time.sleep(10)
                            else:       
                                    print("lift 2 moving, current_floor: {}".format(l2.current_floor))
                        print("lift 2: current_floor: {}".format(l2.current_floor))
                
                else:
                         while l2.current_floor != l2.current_request:
                            time.sleep(1)
                            l2.current_floor = l2.current_floor - 1

                            # handle intermediate requests
                            if l2.current_floor in l2.requests:
                                    print("lift 2 stopped , current_floor: {}".format(l2.current_floor))
                                    l2.requests.remove(l2.current_floor)
                                    time.sleep(10)
                            else:
                                    print("lift 2 moving, current_floor: {}".format(l2.current_floor))
                         print("lift : current_floor: {}".format(l2.current_floor))
                
if __name__ == "__main__":

    lock = threading.Lock()
    t1 = threading.Thread(target=run, args=(lock,))
    t2 = threading.Thread(target=run2, args=(lock,))
    t3 = threading.Thread(target=run3, args=(lock,))
    t1.start()
    t2.start()
    t3.start()

    while True:
        while len(list_of_requests) == 0:
            time.sleep(1)

        request_string = list_of_requests.pop()

        print("request = {}".format(request_string))

        # if person is giving input from inside the lift, format is <floor number>, "lift"<liftnumber>
        if "lift1" in request_string:
                request = int(request_string.split(",")[0])
                l1.requests.append(request)
                continue
        elif "lift2" in request_string:
                request = int(request_string.split(",")[0])
                l2.requests.append(request)
                continue
        else:
                request = int(request_string.split(",")[0])
                
        
        
        diff1 = abs(request - l1.current_floor)
        diff2 = abs(request - l2.current_floor)

        selected_lift = 1 if diff1 <= diff2 else 2

        print("selected lift = {}".format(selected_lift))

        if selected_lift == 1:
                l1.requests.append(request)
        else:
                l2.requests.append(request)
       
        print("lift 1 requests: {}".format(l1.requests))
        print("lift 2 requests: {}".format(l2.requests))


                
