#!/usr/bin/python
import csvops
import time
import os
from colorama import init
from colorama import Fore
import agent
import ghost

"""
References:
colorama - https://www.geeksforgeeks.org/print-colors-python-terminal/
dispMaze - https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e

"""

# Display for debugging
def dispMaze(maze):
    for i in range(numRows):
        for j in range(numCols):
            if (maze[i][j] == unBlkd): # Green for 'u'nblocked cells 
                print(Fore.GREEN + str(maze[i][j]), end=" ")
            elif (maze[i][j] == blkd): # Red for 'b'locked cells
                print(Fore.RED + str(maze[i][j]), end=" ")
            elif (maze[i][j] == "a"):
                print(Fore.YELLOW + str(maze[i][j]), end=" ") 
            else: # For ghosts
                print(Fore.WHITE + str(maze[i][j]), end=" ")

        print("\n")

numRows= 6
numCols = 6
unBlkd = "u"
blkd = "b"

# maze = [["_" for _ in range(numCols)] for _ in range(numRows)]
maze = [[]]

mainMaze = csvops.readCsv(1, numRows, numCols)
print("Maze read from maze1.csv is:\n" + str(mainMaze))

tempMaze = mainMaze

# Spawn the ghost(s)
# For this I may to have take the number of ghosts I am working with and use that to create a list of ghost objects
# This list will then be used when I want to run the game (like when I need to move the agent and ghosts by steps)
g1 = ghost.Ghost("1")
g1.spawnGhost(mainMaze, 6, 6)
g2 = ghost.Ghost("2")
g2.spawnGhost(mainMaze, 6, 6)

# Spawn the agent
a = agent.Agent("agent1")

# Plan a path for the agent
path = a.planPath(mainMaze, (0, 0), (5, 5))
printPath = path
print("The path planned by A* is: " + str(printPath))

init()

dispMaze(tempMaze)

caught = False

# Run the agent/ghost game (based on input params)
while path and not caught:
    os.system("clear") 
    nextCell = path.pop(0)    
    a.moveAgent(nextCell)
    tempMaze[a.row][a.col] = "a"
    if (g1.row == a.row and g1.col == a.col) or (g2.row == a.row and g2.col == a.col):
        caught = True
    g1.moveGhost(mainMaze, 6, 6)
    g2.moveGhost(mainMaze, 6, 6)
    if (g1.row == a.row and g1.col == a.col) or (g2.row == a.row and g2.col == a.col):
        caught = True
    g1Temp = tempMaze[g1.row][g1.col]
    tempMaze[g1.row][g1.col] = g1.name
    g2Temp = tempMaze[g2.row][g2.col]
    tempMaze[g2.row][g2.col] = g2.name
    dispMaze(tempMaze)
    tempMaze[a.row][a.col] = "u"
    tempMaze[g1.row][g1.col] = g1Temp
    tempMaze[g2.row][g2.col] = g2Temp
    time.sleep(1)

if a.row == a.col == 5:
    print(Fore.BLUE + "We reached the goal!")
else:
    print(Fore.MAGENTA + "The ghost got us :(")