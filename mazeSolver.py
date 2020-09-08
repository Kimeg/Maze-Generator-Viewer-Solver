from model import Maze, Cell
from settings import *
import pickle
import sys
import os

def main():
	''' maze id '''
	try:
		i = sys.argv[1] 
	except:
		i = 1

	''' loads specified maze '''
	try:
		maze = pickle.load(open(os.path.join(OUTPUT_DIR, f'maze_{i}.pkl'), 'rb'))
	except Exception as e:
		print(e)
		return

	''' display the process of solving the maze '''
	maze.solve()
	return

if __name__ == '__main__':
	main()
