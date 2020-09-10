''' maze block counts for horizontal and vertical dimensions'''
HN = 25 
VN = 25 

''' screen width and height '''
WIDTH = 600
HEIGHT = 600

''' configurations to fit the maze size regarding the block counts and its ratio with respect to the screen size '''
HSIZE = int(WIDTH*2./3.)
VSIZE = int(HEIGHT*2./3.)

HOFFSET = int((WIDTH-HSIZE)/2)
VOFFSET = int((HEIGHT-VSIZE)/2)

HSTEPSIZE = int(HSIZE/HN)
VSTEPSIZE = int(VSIZE/VN)

''' maze wall width '''
LINEWIDTH = 1

''' frames per second setting for pygame rendering '''
FPS = 60

''' color settings '''
WHITE = (255,255,255)
GRAY = (0,200,200)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,180,0)
BLUE = (0,0,180)
PURPLE = (200,0,200)

''' dict used for searching neighbors or available paths by all directions '''
DIRS = {'down':(0,1), 'up':(0,-1), 'right':(1,0), 'left':(-1,0), 'ul':(-1,-1), 'ur':(1,-1), 'll':(-1,1), 'lr':(1,1)}
#DIRS = {'down':(0,1), 'up':(0,-1), 'right':(1,0), 'left':(-1,0)}

''' output directory for generating mazes '''
OUTPUT_DIR = './mazes'