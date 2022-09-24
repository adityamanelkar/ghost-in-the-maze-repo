#!/usr/bin/python
import random

# This code would have all the necessary setup for spawning the ghost(s)

def spawnGhost(maze, row, col, maxRows, maxCols):
    
    # Need to make sure the ghost is spawned in a cell that is not walled off (i.e. it lies in one of the solution paths for the agent)
    pass

def isValidMove(maze, row, col, maxRows, maxCols):
    
    # Ghost cannot move outside the maze (I'm guessing?)
    pass

def moveGhost(maze, row, col, maxRows, maxCols):
    
    # Here I need to allow for ghosts to move in all four directions
    # Constraints: Ghost can move into a "b"locked cell, but it does so with 0.5 probability or stays in the same cell
    # I'm guessing here, but I think ghost should have a random AI (i.e. it is not an adversary)
    pass