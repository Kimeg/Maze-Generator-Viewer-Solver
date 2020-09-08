from settings import *
import pygame as pg
import numpy as np
import random
import time

pg.init()
CLOCK = pg.time.Clock()
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

class Maze:
    def __init__(self, start, index):
        self.start = start
        self.end = Cell(HN-1, VN-1, HN*VN)
        self.id = index
        self.cur = start
        self.q = [self.cur]

        self.openSet = []
        self.cameFrom = {}
        self.reversePath = []
        self.fillMaze()

    def __repr__(self):
        return f'{self.cur.pos}'

    def fillMaze(self):
        self.cells = {}
        self.cid = {}
        count = 0
        for i in range(HN):
            for j in range(VN):
                count+=1
                self.cells[(i,j)] = Cell(i, j, count)
                self.cid[count] = self.cells[(i,j)]
        return

    def isValid(self, pos):
        return pos[0]>=0 and pos[0]<HN and pos[1]>=0 and pos[1]<VN

    def genPath(self):
        dirs = list(DIRS.keys())
        random.shuffle(dirs)

        found = False
        for d in dirs:
            _from = (self.cur[0], self.cur[1])
            _to = (self.cur[0]+DIRS[d][0], self.cur[1]+DIRS[d][1])

            if self.isValid(_to) and not self.cells[_to].visited:
                found = True 
                break

        if not found:
            self.cur = self.q.pop()
            self.cells[self.cur].backtracked = True
            return

        if d=='left':
            self.cells[_from].left = False
            self.cells[_to].right = False
        elif d=='right':
            self.cells[_from].right = False
            self.cells[_to].left = False
        elif d=='up':
            self.cells[_from].up = False
            self.cells[_to].down = False
        elif d=='down':
            self.cells[_from].down = False
            self.cells[_to].up = False
        self.cells[_to].visited = True
        self.cur = _to
        self.q.append(_to)
        return

    def heuristic(self, cell1, cell2):
        return np.sqrt(np.sum([(cell1.x-cell2.x)**2, (cell1.y-cell2.y)**2]))

    def minF(self):
        ids = [tup for tup in self.fScore.items() if tup[0] in self.openSet]
        self.cur = self.cid[sorted(ids, key=lambda x: x[1])[0][0]]
        return

    def searchNeighbors(self):
        self.neighbors = []
        for k,v in DIRS.items():
            neighbor = Cell(self.cur.x+v[0], self.cur.y+v[1], 0)

            if neighbor.x < 0 or neighbor.x >= HN or neighbor.y < 0 or neighbor.y >= VN:
                continue
            cell = self.cells[neighbor.pos]

            if k=='left' and cell.right:
                continue
            elif k=='right' and cell.left:
                continue
            elif k=='up' and cell.down:
                continue
            elif k=='down' and cell.up:
                continue

            self.neighbors.append(cell)
        return

    def backtrack(self):
        prev = self.cur.id
        while prev in self.cameFrom:
            prev = self.cameFrom[prev]
            self.reversePath.append(prev)
            self.display()
        return

    def solve(self):
        pg.display.set_caption(f'Maze {self.id}')

        self.cur = self.cells[self.start]
        self.openSet = [self.cur.id]
        
        self.cameFrom = {} 

        self.gScore = {cell.id: float('inf') for cell in self.cells.values()} 
        self.gScore[self.cur.id] = 0.

        self.fScore = {cell.id: float('inf') for cell in self.cells.values()} 
        self.fScore[self.cur.id] = self.heuristic(self.cur, self.end)

        while self.openSet:
            self.display()
            self.minF()

            if self.cur == self.end:
                self.backtrack()
                break

            self.openSet.remove(self.cur.id)
            self.searchNeighbors()
            for neighbor in self.neighbors:
                tentative_gScore = self.gScore[self.cur.id] + self.heuristic(self.cur, neighbor)

                if tentative_gScore < self.gScore[neighbor.id]:
                    self.cameFrom[neighbor.id] = self.cur.id
                    self.gScore[neighbor.id] = tentative_gScore
                    self.fScore[neighbor.id] = self.gScore[neighbor.id] + self.heuristic(neighbor, self.end)

                    if not neighbor.id in self.openSet:
                        self.openSet.append(neighbor.id)
        time.sleep(3)
        return

    def display(self):
        SCREEN.fill(BLACK)
        for cell in self.cells.values():
            c = GREEN
            if cell.id in self.openSet or cell.visited:
                c = YELLOW
            if cell.backtracked:
                c = GREEN
            if cell.id in self.cameFrom or self.start==(cell.x, cell.y):
                c = BLUE 
            if isinstance(self.cur, Cell):
                if cell.id == self.cur.id or cell.pos == self.start or cell.id in self.reversePath:
                    c = RED 
            else:
                if self.cur==(cell.x, cell.y):
                    c = RED

            pg.draw.rect(SCREEN, c, (HSTEPSIZE*cell.x + HOFFSET, VSTEPSIZE*cell.y + VOFFSET, HSTEPSIZE, VSTEPSIZE))

            if cell.left:
                pg.draw.line(SCREEN, PURPLE, (HSTEPSIZE*cell.x + HOFFSET, VSTEPSIZE*cell.y + VOFFSET), (HSTEPSIZE*cell.x + HOFFSET, VSTEPSIZE*(1+cell.y) + VOFFSET), LINEWIDTH)
            if cell.right:
                pg.draw.line(SCREEN, PURPLE, (HSTEPSIZE*(1+cell.x) + HOFFSET, VSTEPSIZE*cell.y + VOFFSET), (HSTEPSIZE*(1+cell.x) + HOFFSET, VSTEPSIZE*(1+cell.y) + VOFFSET), LINEWIDTH)
            if cell.up:
                pg.draw.line(SCREEN, PURPLE, (HSTEPSIZE*cell.x + HOFFSET, VSTEPSIZE*cell.y + VOFFSET), (HSTEPSIZE*(1+cell.x) + HOFFSET, VSTEPSIZE*cell.y + VOFFSET), LINEWIDTH)
            if cell.down:
                pg.draw.line(SCREEN, PURPLE, (HSTEPSIZE*cell.x + HOFFSET, VSTEPSIZE*(1+cell.y) + VOFFSET), (HSTEPSIZE*(1+cell.x) + HOFFSET, VSTEPSIZE*(1+cell.y) + VOFFSET), LINEWIDTH)

        CLOCK.tick(FPS)
        pg.display.flip()
        return

class Cell:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.id =index 

        self.pos = (x,y)
        self.left = True 
        self.right = True 
        self.up = True 
        self.down = True 

        self.visited = False
        self.backtracked = False

    def __eq__(self, cell):
        return self.id==cell.id
