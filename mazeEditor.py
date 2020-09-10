from model import Maze, Cell 
from settings import *
import pickle
import sys
import os


def main():
    try:
        i = int(sys.argv[1])
    except:
        i = 1

    try:
        maze = pickle.load(open(os.path.join(OUTPUT_DIR, f'maze_{i}.pkl'), 'rb'))
    except Exception as e:  
        print(e)
        return

    ''' Use mouse to create walls at desired positions '''
    maze.design()
    return

if __name__ == '__main__':
    main()
