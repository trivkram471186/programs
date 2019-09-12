import threading
import time

from enum import Enum

class direction(Enum):
        NONE = 0
        UPWARD = 1
        DOWNWARD = 2

direction_dictionary = {
        "NONE": direction.NONE,
        "UPWARD": direction.UPWARD,
        "DOWNWARD": direction.DOWNWARD
        }

class lift:
        def __init__(self):
            self.current_floor = 0
            self.moving = False
            self.requests = []
            self.current_request = 0
            self.direction = direction.NONE

class request:
        def __init__(self):
                self.floor_number = 0
                self.lift_number = 0
                self.direction = direction.NONE
                self.inside = False

def lift_moving_towards_the_requested_floor(current_request, lift):
        if lift.current_floor < current_request.floor_number and lift.direction  == direction.UPWARD:
                return True
        elif lift.current_floor > current_request.floor_number and lift.direction == direction.DOWNWARD:
                return True
        else:
                return False
        
l1 = lift()
l2 = lift()
current_request = request()

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
                        # lift starts moving in the upward direction
                        l1.moving = True
                        l1.direction = direction.UPWARD
                        
                        while l1.current_floor != l1.current_request:
                                time.sleep(1)
                                l1.current_floor = l1.current_floor + 1

                                # handle intermediate requests
                                if l1.current_floor in l1.requests:
                                        print("lift 1 stopped at floor {}".format(l1.current_floor))
                                        l1.requests.remove(l1.current_floor)
                                        time.sleep(5)
                                else:
                                        print("lift 1 moving, current_floor: {}, direction = {}".format(l1.current_floor, l1.direction))
                        # lift stops
                        l1.moving = False
                        print("lift 1: stopped, current_floor: {}".format(l1.current_floor))
                else:
                        # lift starts moving in the downward direction
                        l1.moving = True
                        l1.direction = direction.DOWNWARD
                        
                        while l1.current_floor != l1.current_request:
                                time.sleep(1)
                                l1.current_floor = l1.current_floor - 1

                                # handle intermediate requests
                                if l1.current_floor in l1.requests:
                                        print("lift 1 stopped at floor {}".format(l1.current_floor))
                                        l1.requests.remove(l1.current_floor)
                                        time.sleep(10)
                                else:
                                        print("lift 1 moving, current_floor: {}, direction = {}".format(l1.current_floor, l1.direction))

                        # lift stops
                        l1.moving = False
                        print("lift 1: stopped, current_floor: {}".format(l1.current_floor))


def run3(lock):
        while True:
                while len(l2.requests) == 0:
                        pass

                l2.current_request = l2.requests.pop()
                if l2.current_floor < l2.current_request:
                        # lift starts moving in the upward direction
                        l2.moving = True
                        l2.direction = direction.UPWARD
                        
                        while l2.current_floor != l2.current_request:
                            time.sleep(1)
                            l2.current_floor = l2.current_floor + 1

                            # handle intermediate requests
                            if l2.current_floor in l2.requests:
                                    print("lift 2 stopped, current_floor: {}".format(l2.current_floor))
                                    l2.requests.remove(l2.current_floor)
                                    time.sleep(10)
                            else:       
                                    print("lift 2 moving, current_floor: {}, direction = {}".format(l2.current_floor, l2.direction))
                                    
                        # lift stops
                        l2.moving = False
                        print("lift 2: stopped, current_floor: {}".format(l2.current_floor))
                
                else:
                         # lift starts moving in the downward direction
                         l2.moving = True
                         l2.direction = direction.DOWNWARD
                         
                         while l2.current_floor != l2.current_request:
                            time.sleep(1)
                            l2.current_floor = l2.current_floor - 1

                            # handle intermediate requests
                            if l2.current_floor in l2.requests:
                                    print("lift 2 stopped , current_floor: {}".format(l2.current_floor))
                                    l2.requests.remove(l2.current_floor)
                                    time.sleep(10)
                            else:
                                    print("lift 2 moving, current_floor: {}, direction = {}".format(l2.current_floor, l2.direction))

                         # lift stops
                         l2.moving = False
                         print("lift 2 : stopped, current_floor: {}".format(l2.current_floor))
                
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

        current_request.floor_number = int(request_string.split(",")[0])
        #request.lift_number        
        current_request.direction = direction_dictionary[request_string.split(",")[2]]

        if "inside" in request_string.split(",")[1]:
                current_request.inside = True

        print("request = {}".format(request_string))

        # if person is giving input from inside the lift, format is <floor number>, "lift"<liftnumber>
        if "inside lift1" in request_string:
                request = int(request_string.split(",")[0])
                l1.requests.append(request)
                continue
        elif "inside lift2" in request_string:
                request = int(request_string.split(",")[0])
                l2.requests.append(request)
                continue
        else:
                request = int(request_string.split(",")[0])
                
        
        # consider the nearest lift among only the lifts that are stationary
        stationary_lifts = [lift for lift in [l1, l2] if lift.moving == False]

        minimum_distance = 9999
        for l in stationary_lifts:
                distance = abs(request - l.current_floor)
                if distance < minimum_distance:
                        minimum_distance = distance
                        nearest_stationary_lift = l
                        
        
        # among the lifts that are moving        
        # consider the nearest lift that is
        # 1. moving towards the requested floor
        # 2. lift direction == request_direction
        moving_lifts = [lift for lift in [l1, l2] if lift.moving == True]

        minimum_distance_moving_lifts = 9999
        for lift in moving_lifts:       
                if((lift_moving_towards_the_requested_floor(current_request, lift) == True) and (lift.direction == current_request.direction)):
                        distance = abs(current_request.floor_number - lift.current_floor)
                        if distance < minimum_distance_moving_lifts :
                                minimum_distance_moving_lifts = distance
                                nearest_moving_lift = lift

        # check whether stationary lift is near or the moving lift
        if minimum_distance_moving_lifts < minimum_distance :
                nearest_lift = nearest_moving_lift
        else:
                nearest_lift = nearest_stationary_lift
                

        nearest_lift.requests.append(current_request.floor_number)
        
        #diff1 = abs(request - l1.current_floor)
        #diff2 = abs(request - l2.current_floor)

        #selected_lift = 1 if diff1 <= diff2 else 2

        #print("selected lift = {}".format(selected_lift))

        #if selected_lift == 1:
         #       l1.requests.append(request)
        #else:
        #        l2.requests.append(request)
       
        #print("lift 1 requests: {}".format(l1.requests))
        #print("lift 2 requests: {}".format(l2.requests))


                
