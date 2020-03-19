'''
Created by Deepti Mahesh
5/10/2019

Main mem = 2
Buffer size = 44
'''

import sys
import time
import random as r
import os
from bisect import bisect

class Node:
	'''
	Node of each tree, has 2 functionality:
		- Split during insertion
		- has 4 pointers to child nodes
	'''

	def __init__(self, mkeys):
		self.keys = list()
		self.parent = None
		self.children = list()
		self.is_leaf = True
		self.next = None
		self.before = None
		self.mkeys = mkeys

	def splitNode(self):
		'''
			Split doen the middle into two seperate nodes, 
			possibly send one higher up.
		'''
		newNode = Node(4)

		mid = self.keys[len(self.keys) // 2]

		if self.is_leaf:
			newNode.is_leaf = True
			self.parent = newNode
			newNode.keys = self.keys[mid:]
			newNode.children =  self.children[mid:]

			self.parent = None
			newNode.next = self.next
			self.next = newNode

			self.keys = self.keys[:mid]
			self.children = self.children[:mid]

			
		else:
			newNode.is_leaf = False
			self.parent = None
			newNode.keys = self.keys[mid+1:]
			newNode.children = self.children[mid+1:]

			self.keys = self.keys[:mid]
			self.children =  self.children[:mid+1]

		return len(self.keys) // 2, newNode

class BTree:

	def __init__(self, factor):
		self.factor = factor
		self.root = Node(mkeys = 4)
		self.root.is_leaf = 1
		self.root.keys = []
		self.root.children = []
		self.root.next = None
		self.root.mkeys = 4


	def execute(self, parsed, arr):
		'''
			Execute the parsed query
		'''
		global output_buffer

		if len(output_buffer) >= 4:
			for op in output_buffer:
				print(op)
			output_buffer = list()

		if parsed[0] == "INSERT":
			tree.prepare_tree(int(parsed[1]))

		elif parsed[0] == "FIND":
			if tree.count_query(int(parsed[1])) != 0:
				output_buffer.append("YES")
			else:
				output_buffer.append("NO")

		elif parsed[0] == "COUNT":
			output_buffer.append(tree.count_query(int(parsed[1])))

		elif parsed[0] == "RANGE":
			miny = int(parsed[1])
			maxy = int(parsed[2])
			output_buffer.append(tree.range_query(miny, maxy))
		return output_buffer
	
	def prepare_tree(self, key):
		'''
			Update new root if any
		'''
		ans, newNode =  self.tree_insert(key, self.root)

		if ans:
			newRoot = Node(mkeys = 4)
			newRoot.keys = list()
			newRoot.is_leaf = False
			newRoot.keys.append(ans)
			newRoot.children = [self.root, newNode]
		
		if ans:
			self.root = newRoot
			return
		else:
			return

	def tree_insert(self, key, node):
		'''
			Bisect node when necessary
		'''

		ans = None

		if node.is_leaf and len(node.keys) <= self.factor-1:
			index = bisect(node.keys, key)
			node.keys[index:index] = [key]
			node.children[index:index] = [key]

			if len(node.keys) <= self.factor-1:
				return None, None
		if node.is_leaf and len(node.keys) > self.factor-1:
			midKey, newNode = node.splitNode()
			return midKey, newNode
		else:
			if key < node.keys[0]:
				ans, newNode = self.tree_insert(key, node.children[0])

			for i in range(len(node.keys) - 1):
				if key >= node.keys[i] and key < node.keys[i + 1]:
					ans, newNode = self.tree_insert(key, node.children[i+1])

			if key >= node.keys[-1]:
				ans, newNode = self.tree_insert(key, node.children[-1])

		if ans:
			index = bisect(node.keys, ans)
			node.keys[index:index] = [ans]
			node.children[index+1:index+1] = [newNode]
			if len(node.keys) <= self.factor-1:
				return None, None
			else:
				midKey, newNode = node.splitNode()
				return midKey, newNode
		else:
			return None, None

	def tree_search_for_query(self, key, node):
		'''
			Search for a query
		'''
		if node.is_leaf:
			return node

		if key <= node.keys[0]:
			return self.tree_search_for_query(key, node.children[0])

		mass = len(node.keys)-1
		for i in range(mass):
			if key>node.keys[i]:
				if key<=node.keys[i+1]:
					return self.tree_search_for_query(key, node.children[i+1])
			else:
				pass

		if key > node.keys[-1]:
			return self.tree_search_for_query(key, node.children[-1])

	def count_query(self, key):
		'''
			Count number of occurences of certain element
		'''
		count = 0

		begin_here = self.tree_search_for_query(key, self.root)

		while begin_here:
			key_count, next_node = self.get_keys_in_range(key, key, begin_here)
			begin_here = next_node
			count += key_count

		return count

	def range_query(self, keyMin, keyMax):
		'''
			Process range query
		'''
		count = 0

		begin_here = self.tree_search_for_query(keyMin, self.root)

		while begin_here:
			key_count, next_node = self.get_keys_in_range(keyMin, keyMax, begin_here)
			begin_here = next_node
			count += key_count

		return count

	def get_keys_in_range(self, keyMin, keyMax, node):
		'''
			Keys in a certain range
		'''
		count = 0

		for i in range(len(node.keys)):
			key = node.keys[i]
			if keyMin <= key:
				if key <= keyMax:
					count += 1
				else:
					continue

		next_node = None

		if len(node.keys) == 0:
			return 0, next_node

		if node.keys[-1] > keyMax:
			next_node = None

		elif node.keys[-1] <= keyMax and node.next:
			next_node = node.next
		
		else:
			next_node = None

		return count, next_node


# Main Function
filename = sys.argv[1]

M, B = 2, 44
pointer_count = 4
buffarray = []
tree = BTree(pointer_count)

input_buffer, output_buffer = [], []

with open(filename) as fh:
	for line in fh:
		parsed = line.strip()
		parsed = parsed.split(" ")
		input_buffer.append(parsed)
		if len(input_buffer) >= 4 :
			for parsed in input_buffer:
				buffArray = tree.execute(parsed, output_buffer)
			input_buffer = list()

	for parsed in input_buffer:
		buffArray = tree.execute(parsed, output_buffer)
	input_buffer = list()

for res in output_buffer:
	print(res)
output_buffer = []