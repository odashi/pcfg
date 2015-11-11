# coding: utf-8

import sys
from collections import defaultdict

def load_model(filename):
	model = defaultdict(lambda: [])
	with open(filename) as fp:
		for l in fp:
			ls = l.strip().split('\t')
			parent = ls[0]
			children = tuple(ls[1].split(' '))
			if len(children) == 1:
				children = children[0]
			score = float(ls[2])
			model[children].append((parent, score))
	return model

def format(tree):
	if isinstance(tree, str):
		return tree
	else: # tuple
		return '(' + ' '.join(format(node) for node in tree) + ')'

def parse(sent, model):
	L = len(sent)
	cky = defaultdict(lambda: [])

	for i in range(L):
		if sent[i] in model:
			cand_list = [((m[0], sent[i]), m[1]) for m in  model[sent[i]]]
		else:
			cand_list = [(('NONE', sent[i]), 0)]
		cand_list2 = []
		for cand in cand_list:
			for rule in model[cand[0][0]]:
				if rule[0][0] != cand[0][0]:
					cand_list2.append(((rule[0], cand[0]), rule[1]+cand[1]))
			
		cky[i, i+1] = sorted(cand_list+cand_list2, key=lambda x: x[1], reverse=True)[:100]
	
	for k in range(2, L+1):
		for i in range(0, L-k+1):
			cand_list = []
			for c in range(i+1, i+k):
				lefts = cky[i, c]
				rights = cky[c, i+k]
				for left in lefts:
					for right in rights:
						key = (left[0][0], right[0][0])
						for rule in model[key]:
							cand_list.append(((rule[0], left[0], right[0]), rule[1]+left[1]+right[1]))
			
			cand_list2 = []
			for cand in cand_list:
				for rule in model[cand[0][0]]:
					if rule[0][0] != cand[0][0]:
						cand_list2.append(((rule[0], cand[0]), rule[1]+cand[1]))

			cky[i, i+k] = sorted(cand_list+cand_list2, key=lambda x: x[1], reverse=True)[:100]
	
	return [t for t in cky[0, L] if t[0][0] == 'ROOT']

def main():
	model = load_model(sys.argv[1])
	for l in sys.stdin:
		ls = l.split()
		for tree, score in parse(ls, model)[:10]:
			pass
			print('%s\t%.10f' % (format(tree), score))
			#print(format(tree))

if __name__ == '__main__':
	main()

