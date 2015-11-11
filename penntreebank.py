# coding: utf-8

import sys
import glob
import math
from collections import defaultdict

def token_generator(filename):
	seq = open(filename).read()
	pos = 0
	paren_list = ['(', ')']

	while pos < len(seq):
		if seq[pos].isspace():
			pos += 1
		elif seq[pos] in paren_list:
			yield seq[pos]
			pos += 1
		else:
			begin = pos
			while pos < len(seq) and not seq[pos].isspace() and seq[pos] not in paren_list:
				pos += 1
			yield seq[begin:pos]

def parse_file(filename):
	stack = []
	for tok in token_generator(filename):
		if tok == '(':
			if stack and stack[-1] == '(': # root
				stack.append('ROOT')
			stack.append(tok)
		elif tok == ')':
			node_list = []
			while True:
				node = stack.pop()
				if node == '(':
					break
				node_list.append(node)

			node_list = node_list[::-1]
			
			while len(node_list) > 3:
				right = node_list.pop()
				left = node_list.pop()
				name = left[0] + '_' + right[0]
				node_list.append((name, left, right))

			new_node = tuple(node_list)
			stack.append(new_node)
		else:
			if stack[-1] == '(':
				tok = tok.split('-')[0]
				if not tok:
					tok = 'NONE'
			stack.append(tok)
	return stack

def count_rules(tree, freq):
	rule = []
	for node in tree:
		if isinstance(node, str):
			rule.append(node)
		else:
			rule.append(node[0])
			count_rules(node, freq)
	freq[tuple(rule)] += 1

def main():
	
	freq = defaultdict(lambda: 0)
	for fname in glob.iglob(sys.argv[1]):
		for tree in parse_file(fname):
			count_rules(tree, freq)

	log_total = math.log(sum(freq.values()))
	#total = defaultdict(lambda: 0)
	#for k, v in freq.items():
	#	total[tuple(k[1:])] += v

	for k, v in freq.items():
		children = tuple(k[1:])
		
		print('%s\t%s\t%.10f' % (k[0], ' '.join(children), math.log(v)-log_total))
		#V = total[children]
		#print('%s\t%s\t%.10f' % (k[0], ' '.join(children), math.log(v)-math.log(V)))

if __name__ == '__main__':
	main()

