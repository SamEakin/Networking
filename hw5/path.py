# path.py
# Networking Homework 5
# Sam Eakin

import sys
import json

class Graph:
	def __init__(self, start, end):
		self.nodes = []
		self.startNode = start
		self.endNode = end
		self.visited = []
		self.unvisited = []

	def nodeExists(self, n):
		for node in self.nodes:
			if n == node.name:
				return True
		else:
			return False

	def createNode(self, name, dest, weight):
		n = Node(name)
		self.nodes.append(n)
		self.unvisited.append(name)
		n.addEdge(dest, weight)

	def getNode(self, name, dest, weight):
		for node in self.nodes:
			if name == node.name:
				node.addEdge(dest, weight)

	def print(self):
		for node in self.nodes:
			print(node)

	def changeWeight(self, name, weight):
		for node in self.nodes:
			if name == node.name:
				#if node.minimumDist >
				node.minimumDist = weight

	def calculateMinimumWeights(self):
		#start at first node
		for node in self.nodes:
			if self.startNode == node.name:
				node.minimumDist = 0 #set start node to 0
				currentMinimum = 999
				for edge in node.edges: #calculate neighbors of start
					self.changeWeight(edge[0], edge[1])
					if int(edge[1]) < currentMinimum:
						currentMinimum = int(edge[1])
						nextNode = edge[0] #find closest neighboring node
						print(nextNode)
						calculateNextNode(nextNode)
				node.visited = True
				self.visited.append(node.name)

	def calculateNextNode(self, nextNode, previousWeight):
		for node in self.nodes:
			if nextNode == node.name:
				for edge in node.edges:
					for n in self.nodes:
						if edge[0] == n.name:
							self.changeWeight(edge[0], edge[1])

							


class Node:
	def __init__(self, name):
		self.name = name
		self.edges = [] #list of tuples (dst, w)
		self.minimumDist = 999
		self.visited = False

	def addEdge(self, dest, weight):
		self.edges.append((dest, weight))

	def __str__(self):
		return 'Node '+self.name+' minimumDist='+str(self.minimumDist)+' edges= '+str(self.edges)

def getInputArgs(): # py path.py [graph.json] [source] [destination]
		arg_count = len(sys.argv)
		print(arg_count)
		if arg_count < 4:
			print("Not enough arguments!")
			sys.exit(-1)
		else:
			file_name = sys.argv[1]
			source = sys.argv[2]
			destination = sys.argv[3]
			return file_name, source, destination


##########################
if __name__ == "__main__":

	file_name, source, destination = getInputArgs()

	network = Graph(source, destination)

	with open(file_name) as json_file:
		data = json.load(json_file)
		for node in data['graph']:
			print('src='+ node['src'] + ' dst='+ node['dst'] + ' w='+ node['w'])
			if network.nodeExists(node['src']):
				network.getNode(node['src'], node['dst'], node['w'])
			else:
				network.createNode(node['src'], node['dst'], node['w'])
	
	network.print()
	network.calculateMinimumWeights()
	network.print()

