import collections
from collections import defaultdict
from pprint import pprint 
import csv
import sys
import random

class Graph:
	def __init__(self):
		self.neighbors = defaultdict(list)
		self.cost = defaultdict(list)
		
	def add_node(self, source, destination, weight):
		self.neighbors[source].append(destination)
		self.cost[source].append(weight)

	def show_graph(self):
		print("Destinations:");pprint(dict(self.neighbors))
		print("Cost:");pprint(dict(self.cost))
	


	def level_order_traversal(self, source, level_size, d_o_a, listOfPatients, degreeCountDict):

		# The BFS queue
		queue = [(source, 0, -1)]

		# keep track of explored nodes
		explored = []
		paths = []
		temp = [0, source]
		paths.append(temp)

		level = [2, 0]
		level_count = 0

		while queue:
	
			level[0] -= 1

			if level[0] <= 0:
				level[0], level[1] = level[1], level[0]

				temp_list = []
				for x in paths:
					if len(x) < level_count + 2:
						continue
					# list of all paths for the level
					temp_list.append(x)

				

				if d_o_a == 'alive':
					temp = max(node for node in temp_list)
					print temp
					# pop out the patientId
					temp.pop(0)
					count = 0

					for patient in listOfPatients:
						temp_patient = list(patient)
						temp_patient.pop(0)
						# print temp_patient

						if set(temp).issubset(temp_patient):
							count += 1
					print "Number of patients who have this pattern is {}".format(count)
					print "\nNumber if Degrees for each word node:"
					for w in temp:
						if w in degreeCountDict:
							print "{} Total: {} Alive: {} Dead: {} Both: {}".format(w, degreeCountDict[w]["Total"], degreeCountDict[w]["Alive"], degreeCountDict[w]["Dead"], degreeCountDict[w]["Both"])

				if d_o_a == 'dead':
					temp = min(node for node in temp_list)
					print temp
					temp.pop(0)
					count = 0
					for patient in listOfPatients:
						temp_patient = list(patient)
						temp_patient.pop(0)
						if set(temp).issubset(temp_patient):
							count += 1
					print "Number of patients who have this pattern is {}".format(count)
					print "\nNumber if Degrees for each word node:"
					for w in temp:
						if w in degreeCountDict:
							print "{} Total: {} Alive: {} Dead: {} Both: {}".format(w, degreeCountDict[w]["Total"], degreeCountDict[w]["Alive"], degreeCountDict[w]["Dead"], degreeCountDict[w]["Both"])
				
				print "Number of edges for this level is {}".format(len(temp_list))

				level_count += 1
				print "current	level is {}".format(level_count)
				print '==========================================='

				if level_count == level_size:
					break

			# Pop the front element of the queue.
			location, cost_till_now, stops_since_source = queue.pop(0)
			element = paths.pop(0)

			if location not in explored:

				# Here we count how many children nodes, each parent node has
				for neighbor, cost in zip(self.neighbors[location], self.cost[location]):
					if explored and neighbor == explored[level_count-1]:
						continue

					temp = list(element)

					level[1] += 1

					temp[0] = cost + cost_till_now
					temp.append(neighbor)
					paths.append(temp)

					queue.append((neighbor, cost + cost_till_now, stops_since_source + 1))

				explored.append(location)

	def print_level_info(d_o_a, temp_list, listOfPatients, degreeCountDict):
		# temp_list.sort(key=lambda x: x[0], reverse=True)
		# print temp_list[0]
		# for x in temp_list:
		# 	print x

		# if d_o_a == 'alive':
		# 	temp_list.sort(key=lambda x: x[0], reverse=True)
		# 	print max(node for node in temp_list)
		# if d_o_a == 'dead':
		# 	temp_list.sort(key=lambda x: x[0])
		# 	print min(node for node in temp_list)

		# if d_o_a == 'alive':
		# 	print max(node for node in temp_list)
		# if d_o_a == 'dead':
		# 	print min(node for node in temp_list)

		if d_o_a == 'alive':
			temp = max(node for node in temp_list)
			print temp
			# pop out the patientId
			temp.pop(0)
			count = 0

			for patient in listOfPatients:
				temp_patient = list(patient)
				temp_patient.pop(0)
				# print temp_patient
				if set(temp).issubset(temp_patient):
					count += 1
					
			print "Number of patients who have this pattern is {}".format(count)
			print "\nNumber if Degrees for each word node:"
			for w in temp:
				if w in degreeCountDict:
					print "{} Total: {} Alive: {} Dead: {} Both: {}".format(w, degreeCountDict[w]["Total"], degreeCountDict[w]["Alive"], degreeCountDict[w]["Dead"], degreeCountDict[w]["Both"])




	def get_rand_val(self, source, level_size):
		# The BFS queue
		queue = [(source, 0, -1)]

		# keep track of explored nodes
		explored = []
		paths = []
		temp = [0, source]
		paths.append(temp)

		level = [2, 0]
		level_count = 0

		while queue:
	
			level[0] -= 1

			if level[0] <= 0:
				level[0], level[1] = level[1], level[0]

				temp_list = []
				for x in paths:
					if len(x) < level_count + 2:
						continue
					temp_list.append(x)

				level_count += 1
				if level_count == level_size:
					break

			# Pop the front element of the queue.
			location, cost_till_now, stops_since_source = queue.pop(0)
			element = paths.pop(0)

			if location not in explored:

				# Here we count how many children nodes, each parent node has
				# d = zip(self.neighbors[location], self.cost[location])
				# neighbor, cost = random.choice(list(d.items()))
				for neighbor, cost in zip(self.neighbors[location], self.cost[location]):
					if explored and neighbor == explored[level_count-1]:
						continue

					temp = list(element)

					level[1] += 1

					temp[0] = cost + cost_till_now
					temp.append(neighbor)
					paths.append(temp)

					queue.append((neighbor, cost + cost_till_now, stops_since_source + 1))

				explored.append(location)



def readTable(track_file, startNode, level_size, d_o_a, listOfPatients, degreeCountDict):
	track = open(track_file, "r")	
	csvReader = csv.reader(track)
	header = csvReader.next()
	index1 = header.index("A_WORD1")
	index2 = header.index("A_WORD2")
	index3 = header.index("D_WORD1")
	index4 = header.index("D_WORD2")
	index5 = header.index("FLAG")
	index6 = header.index("DIFF")
	g = Graph()	
	count = 0
	for row in csvReader:
		var1 = row[index1]
		var2 = row[index2]
		var3 = row[index3]
		var4 = row[index4]
		var5 = row[index5]
		var6 = row[index6]
		if var5 == '1':
			g.add_node(var1, var2, float(var6))				
			count += 1
		elif var5 == '0':
			g.add_node(var3, var4, float(var6))
			count += 1
		# count += 1
		# if count == 3:
		# 	g.show_graph()
		# 	break;
	print "\nNumber of coocurrencies in the graph is {}\n".format(count)
	g.level_order_traversal(startNode, int(level_size), d_o_a, listOfPatients, degreeCountDict)

def readEachPatientKeyWordLists(eachPatientKeyWordFile):
	listOfPatients = []
	fp  = open(eachPatientKeyWordFile)
	for line in fp.readlines():
		temp = []
		for word in line.split(','):
			if word.strip():
				temp.append(word)
		listOfPatients.append(temp)
	return listOfPatients

def countNodeDegrees(cooc_table):
	file = open(cooc_table, "r")
	data = csv.reader(file)
	data.next()

	edges = {}
	ignore = 0

	for row in data:
		if len(row[0]) > 0 and row[2] > ignore:
			if row[0] not in edges:
				edges[row[0]] = {}
			if row[1] not in edges:
				edges[row[1]] = {}
			
			edges[row[0]][row[1]] = 1 # alive
			edges[row[1]][row[0]] = 1 # alive

		if len(row[3]) > 0 and row[5] > ignore:
			if row[3] not in edges:
				edges[row[3]] = {}
			if row[4] not in edges:
				edges[row[4]] = {}

			if row[3] in edges[row[4]]:
				edges[row[3]][row[4]] += 2 # alive and dead
				edges[row[4]][row[3]] += 2 # alive and dead
			else:
				edges[row[3]][row[4]] = 2 # dead
				edges[row[4]][row[3]] = 2 # dead

	count = {}

	for w in edges:
		sum = {1: 0, 2: 0, 3: 0}

		for neighbor in edges[w]:
			sum[edges[w][neighbor]] += 1

		count[w] = {}
		count[w]["Total"] = sum[1] + sum[2] + sum[3]
		count[w]["Alive"] = sum[1]
		count[w]["Dead"] = sum[2]
		count[w]["Both"] = sum[3]

	return count





# -------------------------------------- main function --------------------------------------


# main function called during code execution
# list of patients with keywords: All patients with list of all keywords in their timeline
# argv: 1) list of patients with keywords 2) cooc_table.csv 3) 'oob' 4) 3  5) dead or alive
def main(argv):
	listOfPatientsKeyWords = readEachPatientKeyWordLists(argv[1])
	degreeCountDict = countNodeDegrees(argv[2])

	readTable(argv[2], argv[3], argv[4], argv[5], listOfPatientsKeyWords, degreeCountDict)

if __name__ == '__main__':
	main(sys.argv)
