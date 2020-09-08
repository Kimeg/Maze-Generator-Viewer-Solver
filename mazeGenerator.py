from model import Maze, Cell
from settings import *
import multiprocessing as mp
import pickle
import random
import time
import sys
import os

def genMaze(maze):
    running = True
    while running:
        if len(maze.q)==0:
            break

        maze.genPath()

    with open(os.path.join(OUTPUT_DIR, f'maze_{maze.id}.pkl'), 'wb') as output: 
        pickle.dump(maze, output, pickle.HIGHEST_PROTOCOL) 
    return

def main():
    ''' Maze start position '''
    start = (0,0)

    ''' Number of mazes to generate '''
    try:
        nMaze = int(sys.argv[1])
    except:
        nMaze = 1

    ''' Number of cpus for parallel processing '''
    try:
        nCpu = int(sys.argv[2])
    except:
        nCpu = 1

    ''' list of mazes '''
    mazes = [Maze(start, i+1) for i in range(nMaze)]

    ''' output directory for generated mazes '''
    try:
        os.mkdir(OUTPUT_DIR)
    except Exception as e:
        print(e)
        pass

    ''' Generate desired number of mazes in parallel'''
    pool = mp.Pool(processes=nCpu)
    pool.map(genMaze, mazes)
    pool.close()
    pool.join()
    return

if __name__ == '__main__':
    main()
