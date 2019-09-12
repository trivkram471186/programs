import time
import random

class car:
    def __init__(self):
        self.size = 5

def assign_nearest_slot(floors, floor_number, slot_number):
    flag = 1
    for i in range(len(floors)):
        for j in range(len(floors[i])):
            print("{}, {}".format(i, j))
            if floors[i][j] == ' ':
                floors[i][j] = 'X'
                flag = 0
                break
        if flag == 0:
            break 

def free_slot(floors, floor_number, slot_number):
    floors[floor_number][slot_number] = ' '
    
if __name__ == '__main__':
    
    parking_slots = {}        
    floors = []

    for i in range(5):
        floors.append(["X" for j in range(20)])
        floor = "floor{}".format(i+1)
        parking_slots[floor] = floors[i]

    for i in range(5):
        print("Floor {}: {}".format(i, floors[i]))
              
    
    for i in range(200):
        time.sleep(1)
        choice = random.choice([0, 11])
        random_number = random.randrange(1, 20)
        floor_number = random.choice([0, 1, 2, 3, 4])
        if choice == 0:            
            free_slot(floors, floor_number, random_number)
        else:
            assign_nearest_slot(floors, floor_number, random_number)
        print("i = {}".format(i))
        
        for i in range(5):
            print("Floor {}: {}".format(i, floors[i]))
