#!/usr/bin/python
import random
from colorama import init
from colorama import Fore

import bdbfs
import csvops

"""
References:
colorama - https://www.geeksforgeeks.org/print-colors-python-terminal/
dispMaze - https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e

"""

# Block maze as per the 28/72 rule
def blkMaze(maze):
    for i in range(numRows):
        for j in range(numCols):
            if random.random() < 0.28: # Block the cell with a 28% chance
                maze[i][j] = blkd
    
    # Unblock the START and GOAL cells
    maze[0][0] = unBlkd
    maze[numRows - 1][numCols - 1] = unBlkd

# Here we want to check if it is possible to even reach the goal from the start point!
def isMazeLegit(maze, numRows, numCols):
    return bdbfs.enterTheDragon(maze, numRows, numCols)

# Display for debugging
def dispMaze(maze):
    for i in range(numRows):
        for j in range(numCols):
            if (maze[i][j] == unBlkd): # Green for 'u'nblocked cells 
                print(Fore.GREEN + str(maze[i][j]), end=" ")
            elif (maze[i][j] == blkd): # Red for 'b'locked cells
                print(Fore.RED + str(maze[i][j]), end=" ")
            else: # default unmarked cells (if there are any)
                print(Fore.BLUE + str(maze[i][j]), end=" ")

        print("\n")

# Init variables
unBlkd = "u"
blkd = "b"

numMazes = int(input("Enter the number of 51 * 51 mazes you want to try to generate: "))
fileno = int(input("Enter starting maze file number: "))

numRows = 51
numCols = 51

# Initialize colorama
init()

for _ in range(numMazes):

    maze = [[unBlkd for _ in range(numCols)] for _ in range(numRows)] # We initialize the maze to be unblocked

    """
    !!! LEARNING !!!

    What I was doing with ..

    maze = [[None] * numCols] * numRows 

    .. is not correct!

    Refer to the reasoning in the 31 upvotes answer https://stackoverflow.com/questions/4230000/creating-a-2d-matrix-in-python

    """

    # Generate the blocked spaces in the maze
    blkMaze(maze)

    # Check if the maze is legit using BD-BFS
    if bdbfs.enterTheDragon(maze, numRows, numCols, (numRows - 1, numCols - 1)):
        print(Fore.BLUE + "Everything is good with the world!\nSo saving a CSV file for future reference")
        # Since legit maze, we want to save it in a CSV
        csvops.generateCsv(maze, fileno)
        fileno += 1

    # Display the generated maze
    dispMaze(maze)

# Finish!