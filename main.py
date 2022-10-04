#!/usr/bin/python
import csvops
import time
import os
from colorama import init
from colorama import Fore
import agent
import ghost
import pandas as pd

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

numRows= 11
numCols = 11
unBlkd = "u"
blkd = "b"
firstMaze = 1
lastMaze = 30

no_of_Ghost = 4
Agent_No = 1
survivalList = []

init()

# maze = [["_" for _ in range(numCols)] for _ in range(numRows)]
# maze = [[]]

for mazeNo in range(firstMaze, lastMaze + 1):

    currentMaze = csvops.readCsv(mazeNo, numRows, numCols)
    # print("Maze read from maze" + str(mazeNo) + ".csv is:\n" + str(currentMaze))

    # Spawn the ghost(s)
    # For this I may to have take the number of ghosts I am working with and use that to create a list of ghost objects
    # This list will then be used when I want to run the game (like when I need to move the agent and ghosts by steps)
    ghosts = [ghost.Ghost(str(i)) for i in range(no_of_Ghost)]

    for g in ghosts:
        g.spawnGhost(currentMaze, numRows, numCols)

    # Spawn the agent
    a = agent.Agent("agent" + str(Agent_No))

    dispMaze(currentMaze)

    # Plan a path for the agent
    path = a.planPath(currentMaze, (0, 0), (numRows - 1, numCols - 1))
    print("The path planned by A* is: " + str(path))

    caught = False

    # Run the agent/ghost game (based on input params)
    while path and not caught:
        # os.system("clear") 
        
        nextCell = path.pop(0)    
        
        if a.name == "agent1":
            a.moveAgent(nextCell)
        # For other agents movement strategy will differ

        # currentMaze[a.row][a.col] = "a"

        for g in ghosts:
            if g.row == a.row and g.col == a.col:
                caught = True
                break

        for g in ghosts:
            g.moveGhost(currentMaze, 11, 11)

        for g in ghosts:
            if g.row == a.row and g.col == a.col:
                caught = True
                break

        # g1Temp = currentMaze[g1.row][g1.col]
        # currentMaze[g1.row][g1.col] = g1.name
        # g2Temp = currentMaze[g2.row][g2.col]
        # currentMaze[g2.row][g2.col] = g2.name
        # dispMaze(currentMaze)
        # currentMaze[a.row][a.col] = "u"
        # currentMaze[g1.row][g1.col] = g1Temp
        # currentMaze[g2.row][g2.col] = g2Temp
        # time.sleep(1)
        
    # End movement

    if a.row == a.col == 10:
        print(Fore.BLUE + "We reached the goal!")
        survivalList.append(1)
    else:
        print(Fore.MAGENTA + "The ghost got us :(")
        survivalList.append(0)

df = pd.DataFrame(survivalList)
df.columns = ["Survivability"]

file_name = "./agent_csv/agent" + str(Agent_No) + "/Ghost" + str(no_of_Ghost) + '.csv'
df.to_csv(file_name, encoding='utf-8')
