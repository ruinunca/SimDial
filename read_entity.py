#!/usr/bin/env python

import sys
import json
import pdb


if len(sys.argv) == 1:
	sys.argv = ["", "1500_data_fixed/movie-MixSpec-15.json"]

def main():
	file_path = sys.argv[1]

	json_file = open(file_path)
	dials = json.loads(json_file.read())

	# entities = {}

	# for dial in dials:
	# 	# last_turn = dial['dial'][-1]
	# 	for slu in dial['dial'][-1]['usr']['slu']:
	# 		slot_name = slu['slots'][0][0]
	# 		slot_value = slu['slots'][0][1]
	# 		if slot_name in entities:
	# 			entities[slot_name]['num'] += 1
	# 			if slot_value in entities[slot_name]['val']:
	# 				entities[slot_name]['val'][slot_value] += 1
	# 			else:
	# 				entities[slot_name]['val'][slot_value] = 1
	# 		else:

	# 			entities[slot_name]= {'num':1, 'val':{}}

	# for name in entities:
	# 	print(name, entities[name]['num'])

	# 	for val in entities[name]['val']:
	# 		print('     ', val, entities[name]['val'][val])
	# # for name in entities:
	# # 	for val in entities[name]['val']:
	# # 		print(val, entities[name]['val'][val])


	############# count how many turn in a conversation #################
	turn_num = []
	for dial in dials:
		turn_num.append(dial['dial'][-1]['turn'])
	print(turn_num, sum(turn_num[:9]))



if __name__ == "__main__":
	main()
