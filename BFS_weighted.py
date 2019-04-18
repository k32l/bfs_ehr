"""
We will initialize the BFS queue with the given location as the starting point. 
We then perform the breadth first traversal, and keep going until the queue is 
empty or until the maximum number of stops have been exhausted.
"""
import collections
from collections import defaultdict
from pprint import pprint 
class FlightNetwork:
	def __init__(self):
		self.neighbors = defaultdict(list)
		self.cost = defaultdict(list)
		
	def add_flight(self, source, destination, price):
		self.neighbors[source].append(destination)
		self.cost[source].append(price)
	
	def show_flights(self):
		# print("Destinations:");pprint(dict(self.neighbors))
		# print("Cost:");pprint(dict(self.cost))
		return self.neighbors, self.cost


	# Code for the BFS algorithm
	def bfs(self, source, visited):
        	visited[source] = 1
        	for destination, cost in zip(self.neighbors[source], self.cost[source]):
        		if destination not in visited:
        			self.bfs(destination, visited)
	
	"""
	This function is used to backtrack the nodes in the parent dictionary to find out all 
    routes from S to D of varying lengths. The starting point (D, k) determines the length of 
    paths that would be found by this function. Length would be k. So we
    have to have a for loop from min stops to max stops to get all the routes.
	"""
	# destination = ('F', 2)
	def get_route(self, destination, source, parent):
		if destination[0] == source:
			return [source]	
		routes = []
		for p in parent[destination]:
			print "loop p = {}".format(p)
			for r in self.get_route(p, source,  parent):
				print "loop r = {}".format(p)
				routes.extend([r + "-->" + destination[0]])
			# routes.extend([r + "-->" + destination[0] for r in self.get_route(p, source,  parent)])
		return routes

	"""
	Classic level order traversal 
    * source represents S i.e. the starting point of our flight.
    * destination is D i.e. the ending point of our route.
    * stops_range is a tuple representing minimum and maximum number of stops required in the required flight routes.
	"""
	def level_order_traversal(self, source, destination, stops_range):
		least_stops, max_stops = stops_range

		# The BFS queue
		queue = [(source, 0, -1)]
		# queue = collections.deque[(source, 0, -1)]
		# Parent dictionary used for finding the actual routes once level order traversal is done
		parent = defaultdict(list)

		"""
		Do swapping to track the size of levels. (x1,x2),where x1 is the number of nodes 
		on the current level and x2 is the number of nodes on the next level. Subtract x1 
		on each traverse and and it's nodes to x2. When x1 == 0. The level is finished,  
		swap numbers and repeat the process
		"""
		level = [2, 0]
		level_count = 0

		# Continue until the queue is empty
		while queue:
			print '==========================================='
			
			print "queue = {}".format(queue)
			# Pop the front element of the queue.
			location, cost_till_now, stops_since_source = queue.pop(0)
			print "location = {}, cost_till_now = {}, stops_since_source = {}".format(location, cost_till_now, stops_since_source)
			# location, cost_till_now, stops_since_source = queue.popleft()
			level[0] -= 1
			if level[0] <= 0:
				print "level[0] = {}, level[1] = {}".format(level[0], level[1])
				level[0], level[1] = level[1], level[0]
				level_count += 1
				print "current	level is {}".format(level_count)
			# If the current location has any neighbors i.e. any direct flights, iterate over those neighbors
			if location in self.neighbors:
				print("Destinations:");pprint(dict(self.neighbors))
				print("Cost:");pprint(dict(self.cost))
				# level[0] -= 1

				# Here we count how many children nodes, each parent node has
				for neighbor, cost in zip(self.neighbors[location], self.cost[location]):
					
					level[1] += 1
					print "For each node level[0] = {}, level[1] = {}".format(level[0], level[1])
					print "neighbor = {}, cost = {}".format(neighbor, cost)
					"""
                    THIS STEP IS VERY IMPORTANT. We record all the parents of this `location` via which a path
                    starting from S reached `location` in `stops_since_source + 1` steps.
                	"""
					parent[(neighbor, stops_since_source + 1)].append((location, stops_since_source))
					print "parent:";pprint(dict(parent))

					# If the number of stops till now is < max_stops, then we can add this `location` node for processing.
					if stops_since_source < max_stops:
						print "neighbor = {}, cost + cost_till_now = {}, stops_since_source + 1 = {}".format(neighbor, cost + cost_till_now, stops_since_source + 1)
						queue.append((neighbor, cost + cost_till_now, stops_since_source + 1))

		# Return parent node for route backtracking.
		# print "parent";pprint(dict(parent))
		return parent




f = FlightNetwork()

# f.add_flight('Los Angeles', 'New Delhi', 200)
# f.add_flight('Los Angeles', 'Japan', 87)
# f.add_flight('Germany', 'New Delhi', 125)
# f.add_flight('Italy', 'Los Angeles', 150)
# f.add_flight('New Delhi', 'France', 100)
# f.add_flight('Los Angeles', 'France', 200)
# f.add_flight('Italy', 'New Delhi', 300)
# f.add_flight('France', 'Norway', 175)
# f.add_flight('Ireland', 'Chicago', 100)
# f.add_flight('Chicago', 'Italy', 135)
# f.add_flight('Los Angeles', 'Ireland', 100)
# f.add_flight('Ireland', 'New Delhi', 200)


# =========================================
f.add_flight('A', 'C', 10)
f.add_flight('A', 'B', 20)
f.add_flight('A', 'F', 14)
f.add_flight('B', 'D', 20)
f.add_flight('C', 'B', 120)
f.add_flight('C', 'M', 200)
f.add_flight('D', 'C', 75)
f.add_flight('C', 'E', 145)
f.add_flight('C', 'F', 50)
f.add_flight('D', 'E', 45)
f.add_flight('D', 'F', 60)
f.add_flight('M', 'F', 45)
f.add_flight('E', 'F', 60)

# neighbors_dict = {}
# cost_dict = {}

# neighbors_dict, cost_dict = f.show_flights()

# pprint(dict(neighbors_dict))
# pprint(dict(cost_dict))

parent = f.level_order_traversal('A', 'F', (2,3))

# for r in range(2, 4):
#     print("\nFlights with {} stops in between are as follows:".format(r))
#     routes = f.get_route(('F', r), 'A', parent)
#     for r in routes:
#         print(r)