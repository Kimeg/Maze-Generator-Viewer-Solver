# Maze Generator/Viewer/Solver
 This is a python based maze simulation project intended for generating mazes, viewing them, and solving them.
 Future updates expected to include dynamic functionalities such as maze design by using mouse and applying 
 different types of path-searching algorithms.

Usage:

Generate Maze

$ python mazeGenerator.py [number of mazes to generate] [number of CPUs for parallel processing]
$ python mazeGenerator.py  # both inputs are optional, default values are 1 maze and 1 CPU.

View Maze

$ python mazeViewer.py [an integer (maze ID) for viewing the maze]
$ python mazeViewer.py  # without input, all generated mazes are viewed.

Solve Maze

$ python mazeSolver.py [an integer (maze ID) for solving the maze and viewing the process]
$ python mazeSolver.py  # without input, maze 1 is solved by default.

Modify settings.py according to your needs.
