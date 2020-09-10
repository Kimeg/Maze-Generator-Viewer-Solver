from model import Maze, Cell 
from settings import *
import pickle
import sys
import os


def main():
    start = (0,0)

    try:
        os.mkdir(OUTPUT_DIR)
    except Exception as e:
        print(e)
        pass

    index = len(os.listdir(OUTPUT_DIR))+1

    ''' Generate a template maze '''
    maze = Maze(start, index)

    ''' initialize all cells as open ones '''
    maze.openAll()

    ''' Use mouse to create walls at desired positions '''
    maze.design()
    return

if __name__ == '__main__':
    main()
