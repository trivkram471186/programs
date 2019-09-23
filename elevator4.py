import threading
import time

from enum import Enum

# constants
INSIDE = "inside"
INSIDE_LIFT1 = "inside lift1"
INSIDE_LIFT2 = "inside lift2"

class direction(Enum):
        NONE = 0
        UPWARD = 1
        DOWNWARD = 2
        
d = direction

direction_dictionary = {
        "NONE": direction.NONE,
        "UPWARD": direction.UPWARD,
        "DOWNWARD": direction.DOWNWARD
        }

class lift:
        def __init__(self):
            self.lift_number = 0
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


l1 = lift()
l2 = lift()

l1.lift_number = 1
l2.lift_number = 2

current_request = request()

list_of_requests = []

def lift_moving_towards_the_requested_floor(current_request, lift):
        if lift.current_floor < current_request.floor_number and lift.direction  == direction.UPWARD:
                return True
        elif lift.current_floor > current_request.floor_number and lift.direction == direction.DOWNWARD:
                return True
        else:
                return False       


def process_request(lift):
       
               # while len(lift.requests) == 0:
               #         print("process_request(lift): lift {} requests = {}".format(lift.lift_number, lift.requests))
               #         time.sleep(1)
               #         pass

                if len(lift.requests) == 0 :
                        return
                
                print("process_request(lift)")
                time.sleep(0.5)
                
                lift.current_request = lift.requests.pop()
                if lift.current_floor < lift.current_request:
                        # lift starts moving in the upward direction
                        lift.moving = True
                        lift.direction = direction.UPWARD
                        
                        while lift.current_floor != lift.current_request:
                                time.sleep(1)
                                lift.current_floor = lift.current_floor + 1

                                # handle intermediate requests
                                if lift.current_floor in lift.requests:
                                        print("lift {} stopped at floor {}".format(lift.lift_number, lift.current_floor))
                                        lift.requests.remove(lift.current_floor)
                                        time.sleep(5)
                                else:
                                        print("lift {} moving, current_floor: {}, direction = {}".format(lift.lift_number, lift.current_floor, lift.direction))
                        # lift stops
                        lift.moving = False
                        print("lift {}: stopped, current_floor: {}".format(lift.lift_number, lift.current_floor))
                else:
                        # lift starts moving in the downward direction
                        lift.moving = True
                        lift.direction = direction.DOWNWARD
                        
                        while lift.current_floor != lift.current_request:
                                time.sleep(1)
                                lift.current_floor = lift.current_floor - 1

                                # handle intermediate requests
                                if lift.current_floor in lift.requests:
                                        print("lift {} stopped at floor {}".format(lift.lift_number, lift.current_floor))
                                        lift.requests.remove(lift.current_floor)
                                        time.sleep(10)
                                else:
                                        print("lift {} moving, current_floor: {}, direction = {}".format(lift.lift_number, lift.current_floor, lift.direction))

                        # lift stops
                        lift.moving = False
                        print("lift {}: stopped, current_floor: {}".format(lift.lift_number, lift.current_floor))



def run():
    while True:
        i = input()
       
        list_of_requests.append(i)

        print("list of requests = {}".format(list_of_requests))
       
def run2(lock1):
        while True:
                lock1.acquire()
                process_request(l1)
                lock1.release()
                print("lift 1 requests = {}".format(l1.requests))
                print("len(l1.requests) = {}".format(len(l1.requests)))

                if len(l1.requests) == 0 :
                        print("Thread for lift 1 completed");
                        return
        
def run3(lock2):
        while True:
                lock2.acquire()
                process_request(l2)
                lock2.release()
                print("lift 2 requests = {}".format(l2.requests))
                print("len(l2.requests) = {}".format(len(l2.requests)))

                if len(l2.requests) == 0 :
                        print("Thread for lift 2 completed");
                        return
        
if __name__ == "__main__":

    lock1 = threading.Lock()
    lock2 = threading.Lock()

    t1 = threading.Thread(target=run, args=())
    t2 = threading.Thread(target=run2, args=(lock1,))
    t3 = threading.Thread(target=run3, args=(lock2,))

    t2._event = threading.Event()
    t3._event = threading.Event()
    
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

        if INSIDE in request_string.split(",")[1]:
                current_request.inside = True

        print("request = {}".format(request_string))

        # if person is giving input from inside the lift, format is <floor number>, "lift"<liftnumber>
        if INSIDE_LIFT1 in request_string:
                request = int(request_string.split(",")[0])
                l1.requests.append(request)
                continue
        elif INSIDE_LIFT2 in request_string:
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



       # if len(l1.requests) != 0 :
        #        t2._event.set()
         #       print("l1.requests != 0, t2 = {}".format(t2))
       # else:
        #        t2._event.clear()
         #       print("l1.requests == 0, t2 = {}".format(t2))

         # start the threads for each lift if it has pending requests
         
        if len(l1.requests) != 0 :
                  t2 = threading.Thread(target=run2, args=(lock1,))
                  print("Thread for lift 1 starting, {}".format(t2))
                  t2.start()

        if len(l2.requests) != 0 :
                  t3 = threading.Thread(target=run3, args=(lock2,))
                  print("Thread for lift 2 starting, {}".format(t3))
                  t3.start()                    

        

                
