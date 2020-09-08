from model import Maze, Cell
from settings import *
import multiprocessing as mp
import pygame as pg
import pickle
import random
import time
import sys
import os

''' Display all generated mazes '''
def main():
    ''' Time interval between each maze rendering '''
    TI = 0.3

    ''' input : view specified maze ; no-input : view all mazes '''
    view_all = False
    try:
        i = int(sys.argv[1])
    except:
        N = len(os.listdir(OUTPUT_DIR))
        view_all = True

    if view_all:
        for j in range(1, N+1):
            try:
                maze = pickle.load(open(os.path.join(OUTPUT_DIR, f'maze_{j}.pkl'), 'rb'))
            except Exception as e:
                print(e)
                continue
            pg.display.set_caption(f'Maze {j}')

            maze.display()
            time.sleep(TI)
    else:
        try:
            maze = pickle.load(open(os.path.join(OUTPUT_DIR, f'maze_{i}.pkl'), 'rb'))
        except Exception as e:
            print(e)
            return
        pg.display.set_caption(f'Maze {i}')

        maze.display()
        time.sleep(TI)
    pg.quit()
    return

if __name__ == '__main__':
    main()
