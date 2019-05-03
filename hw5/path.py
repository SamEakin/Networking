# path.py
# Networking Homework 5
# Sam Eakin

import json

class Graph:
	def __init__(self):
		self.nodes = []
		self.visited = []
		self.unvistited = []

	def nodeExists(self, n):
		for node in self.nodes:
			#print('Checking if '+n+' matches '+node.name)
			if n == node.name:
				return True
		else:
			return False

	def createNode(self, name, dest, weight):
		n = Node(name)
		self.nodes.append(n)
		n.addEdge(dest, weight)

	def getNode(self, name, dest, weight):
		for node in self.nodes:
			if name == node.name:
				node.addEdge(dest, weight)

	def print(self):
		for node in self.nodes:
			print(node)


class Node:
	def __init__(self, name):
		self.name = name
		self.edges = [] #list of tuples (dst, w)

	def addEdge(self, dest, weight):
		self.edges.append((dest, weight))

	def __str__(self):
		return 'Node '+self.name+' edges = '+str(self.edges)

##########################
if __name__ == "__main__":

	network = Graph()

	with open('graph.json') as json_file:
		data = json.load(json_file)
		for node in data['graph']:
			print('src='+ node['src'] + ' dst='+ node['dst'] + ' w='+ node['w'])
			if network.nodeExists(node['src']):
				print('Node Exists! Adding new edge to node.')
				network.getNode(node['src'], node['dst'], node['w'])
			else:
				print('Node Does Not Exist. Creating new Node.')
				network.createNode(node['src'], node['dst'], node['w'])
		network.print()

