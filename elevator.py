import threading
import time

class lift:
	def __init__(self):
		self.current_floor = 0
		self.moving = False

l1 = lift()
l2 = lift()

list_of_requests = []

def run():

	while True:

		i = input()

		list_of_requests.append(i)

		print(list_of_requests)
		print(len(list_of_requests))

	
if __name__ == "__main__":
	
	t1 = threading.Thread(target=run)

	t1.start()

	# process each request
	while True:
		while(len(list_of_requests) == 0):
			#do nothing
			time.sleep(2)

		request = list_of_requests.pop()

		print(request)
		# compute the nearest lift
		diff1 = abs(l1.current_floor - request)
		diff2 = abs(l2.current_floor - request)
		
		print("diff1 = {}".format(diff1))
		print("diff2 = {}".format(diff2))

		lift_no = 1 if (diff1 <= diff2) else 2

		print("lift1 current_floor = {}".format(l1.current_floor))

		print("lift no = {}".format(lift_no))
		if(lift_no == 1):
			if l1.current_floor < request:
				for i in range(l1.current_floor, request):
					time.sleep(2)
					l1.current_floor = l1.current_floor + 1
					print("Lift1 moving, current_floor = {}".format(l1.current_floor))

			else:
				while l1.current_floor != request:
					time.sleep(2)
					l1.current_floor = l1.current_floor - 1
					print("Lift1 moving, current_floor = {}".format(l1.current_floor))
		else:
			if l2.current_floor < request :
				while l2.current_floor != request:
					time.sleep(2)
					l2.current_floor = l2.current_floor + 1
					print("Lift2 moving, current_floor = {}".format(l2.current_floor))
			else:	
				while l2.current_floor != request:
					time.sleep(2)
					l2.current_floor = l2.current_floor - 1
					print("Lift2 moving, current_floor = {}".format(l2.current_floor))
				
		