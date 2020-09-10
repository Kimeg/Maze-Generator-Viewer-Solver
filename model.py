from settings import *
import pygame as pg
import numpy as np
import random
import pickle
import time
import os

pg.init()
CLOCK = pg.time.Clock()
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

class Maze:
    def __init__(self, start, index):
        self.start = start
        self.end = None 
        self.id = index
        self.cur = start
        self.q = [self.cur]

        self.openSet = []
        self.cameFrom = {}
        self.reversePath = []
        self.selected = []
        
        self.HN = HN
        self.VN = VN
        self.HSTEPSIZE = HSTEPSIZE 
        self.VSTEPSIZE = VSTEPSIZE 
        self.HOFFSET = HOFFSET
        self.VOFFSET = VOFFSET

        self.fillMaze()

    def __repr__(self):
        return f'{self.cur.pos}'

    def openAll(self):
        for cell in self.cells.values():
            cell.openAll()
        return
    
    def mapCoords(self, tup):
        x, y = tup
        return (int((x-self.HOFFSET)/self.HSTEPSIZE),int((y-self.VOFFSET)/self.VSTEPSIZE))

    def design(self):
        running = True 
        count = 0 
        while running:
            count+=1
            for event in pg.event.get():
                if event==pg.QUIT:
                    running = False
                    break
                if event==pg.MOUSEBUTTONDOWN:   
                    print('btn')

            if pg.mouse.get_pressed()[0]:
                pos = self.mapCoords(pg.mouse.get_pos())
                cell = self.cells[pos]
                if cell.all_open: 
                    self.cells[pos].closeAll()
                    self.selected.append(self.cells[pos].id)
                else:
                    print('already closed')

            if pg.mouse.get_pressed()[2]:
                pos = self.mapCoords(pg.mouse.get_pos())
                cell = self.cells[pos]
                if cell.all_open: 
                    print('already open')
                else:
                    self.cells[pos].openAll()
                    self.selected.remove(self.cells[pos].id)

            if pg.mouse.get_pressed()[1]:
                break

            CLOCK.tick(FPS)
            self.display()
            pg.display.flip()
        pg.quit() 
        with open(os.path.join(OUTPUT_DIR, f'maze_{self.id}.pkl'), 'wb') as output: 
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        print(f'\nA new maze with ID : {self.id} has been created.\n')
        return

    def fillMaze(self):
        self.cells = {}
        self.cid = {}
        count = 0
        for i in range(self.HN):
            for j in range(self.VN):
                count+=1
                self.cells[(i,j)] = Cell(i, j, count)
                self.cid[count] = self.cells[(i,j)]
        return

    def isValid(self, pos):
        return pos[0]>=0 and pos[0]<self.HN and pos[1]>=0 and pos[1]<self.VN

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
        dirs = list(DIRS.keys())
        random.shuffle(dirs)
        self.neighbors = []
        for k in dirs:
            v = DIRS[k]
            neighbor = Cell(self.cur.x+v[0], self.cur.y+v[1], 0)

            if neighbor.x < 0 or neighbor.x >= self.HN or neighbor.y < 0 or neighbor.y >= self.VN:
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
            elif k=='ul':
                if not cell.all_open:
                    continue
                n1 = self.cells[(cell.x+1, cell.y)]
                n2 = self.cells[(cell.x, cell.y+1)]
                if n1.down and n2.right:
                    continue
            elif k=='ur':
                if not cell.all_open:
                    continue
                n1 = self.cells[(cell.x-1, cell.y)]
                n2 = self.cells[(cell.x, cell.y+1)]
                if n1.down and n2.left:
                    continue
            elif k=='ll':
                if not cell.all_open:
                    continue
                n1 = self.cells[(cell.x+1, cell.y)]
                n2 = self.cells[(cell.x, cell.y-1)]
                if n1.up and n2.right:
                    continue                                
            elif k=='lr':
                if not cell.all_open:
                    continue
                n1 = self.cells[(cell.x-1, cell.y)]
                n2 = self.cells[(cell.x, cell.y-1)]
                if n1.up and n2.left:
                    continue

            self.neighbors.append(cell)
        return

    def solve(self, start, end):
        pg.display.set_caption(f'Maze {self.id}')
        self.start = start.pos
        self.end = end

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

            if pg.mouse.get_pressed()[1]:
                return 
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
        time.sleep(2)
        return

    def backtrack(self):
        prev = self.cur.id
        while prev in self.cameFrom:
            prev = self.cameFrom[prev]
            self.reversePath.append(prev)
            self.display()
        return

    def display(self):
        SCREEN.fill(BLACK)
        for cell in self.cells.values():
            c = GREEN
            if cell.id in self.openSet or cell.visited or cell.id in self.selected:
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

            pg.draw.rect(SCREEN, c, (self.HSTEPSIZE*cell.x + self.HOFFSET, self.VSTEPSIZE*cell.y + self.VOFFSET, self.HSTEPSIZE, self.VSTEPSIZE))

            if cell.left:
                pg.draw.line(SCREEN, PURPLE, (self.HSTEPSIZE*cell.x + self.HOFFSET, self.VSTEPSIZE*cell.y + self.VOFFSET), (self.HSTEPSIZE*cell.x + self.HOFFSET, self.VSTEPSIZE*(1+cell.y) + self.VOFFSET), LINEWIDTH)
            if cell.right:
                pg.draw.line(SCREEN, PURPLE, (self.HSTEPSIZE*(1+cell.x) + self.HOFFSET, self.VSTEPSIZE*cell.y + self.VOFFSET), (self.HSTEPSIZE*(1+cell.x) + self.HOFFSET, self.VSTEPSIZE*(1+cell.y) + self.VOFFSET), LINEWIDTH)
            if cell.up:
                pg.draw.line(SCREEN, PURPLE, (self.HSTEPSIZE*cell.x + self.HOFFSET, self.VSTEPSIZE*cell.y + self.VOFFSET), (self.HSTEPSIZE*(1+cell.x) + self.HOFFSET, self.VSTEPSIZE*cell.y + self.VOFFSET), LINEWIDTH)
            if cell.down:
                pg.draw.line(SCREEN, PURPLE, (self.HSTEPSIZE*cell.x + self.HOFFSET, self.VSTEPSIZE*(1+cell.y) + self.VOFFSET), (self.HSTEPSIZE*(1+cell.x) + self.HOFFSET, self.VSTEPSIZE*(1+cell.y) + self.VOFFSET), LINEWIDTH)

        CLOCK.tick(FPS)
        pg.display.flip()
        return

class Cell:
    def __init__(self, x, y, index=None):
        self.x = x
        self.y = y
        self.id =index 

        self.pos = (x,y)
        self.closeAll()

        self.visited = False
        self.backtracked = False

    def openAll(self):
        self.left = False 
        self.right = False 
        self.up = False 
        self.down = False 
        self.all_open = True 

    def closeAll(self):
        self.left = True 
        self.right = True 
        self.up = True 
        self.down = True 
        self.all_open = False 

    def __eq__(self, cell):
        return self.pos==cell.pos
