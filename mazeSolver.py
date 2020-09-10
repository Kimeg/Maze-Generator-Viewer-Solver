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

	''' set start and goal for the maze '''
	start = Cell(0, 0)
	goal = Cell(maze.HN-1, maze.VN-1)

	''' display the process of solving the maze '''
	maze.solve(start, goal)
	return

if __name__ == '__main__':
	main()
