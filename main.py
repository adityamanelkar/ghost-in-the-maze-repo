#!/usr/bin/python
import csvops
import math
import copy
from colorama import init
from colorama import Fore
import agent
import ghost
import pandas as pd
import datetime

"""
References:
colorama - https://www.geeksforgeeks.org/print-colors-python-terminal/
dispMaze - https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e

"""
# Find possible children for Monte Carlo (Agent 3)
def findChildren(maze, a, ghosts) -> list:
    """
    Return valid children of agent a
    """
    children = []
    current = (a.row, a.col)

    xDelta = [0, 1, 0, -1]
    yDelta = [1, 0, -1, 0]

    for i in range(4):
        breakCnt = 0
        child = (current[0] + xDelta[i], current[1] + yDelta[i])
        
        # If we go out of bounds
        if child[0] < 0 or child[1] < 0 or child[0] >= len(maze) or child[1] >= len(maze[0]):
            continue
            
        # If cell is blocked
        if maze[child[0]][child[1]] == "b":
            continue

        # If there is a ghost in the cell
        for ghost in ghosts:
            if child == (ghost.row, ghost.col):
                breakCnt += 1
                break
        
        if breakCnt == 0:
            children.append(child)

    return children

# Find utility values for children
def monteCarlo(maze, a, children, gs, agentBasis="agent3", maxSteps=1001) -> tuple:
    """
    Compare utilities for each of the children of a and return the coordinates of the child w/ highest utility
    """
    import ghost

    # Map with utility values (asked Aravind and he said it was better to recalculate it - so didn't make it global)
    utility = {}

    numRows = len(maze)
    numCols = len(maze[0])

    bestChild = (a.row, a.col)
    maxUtility = 0

    ghostSet = set([])

    if agentBasis == "agent3" or agentBasis == "agent4" or agentBasis == "agent5":

        for child in children:

            utilityList = []

            # I want to run 100 sims at the moment to calculate average utilities
            for i in range(100):

                # By default set the agent as not caught
                caught = False

                simA = copy.deepcopy(a)

                (simA.row, simA.col) = child # Make sure our current simulation starts with current child

                simGhosts = [ghost.Ghost(str(i)) for i in range(len(gs))]

                for simGhost, g in zip(simGhosts, gs):
                    simGhost = copy.deepcopy(g)

                for simGhost in simGhosts:
                    simGhost.moveGhost(maze, numRows, numCols) # Simulate moving the ghosts once as wel
                    ghostSet.add((simGhost.row, simGhost.col))

                for simGhost in simGhosts:
                    if simGhost.row == simA.row and simGhost.col == simA.col:
                        caught = True

                # Plan a path for the agent
                if agentBasis == "agent3":
                    path = simA.planPath(maze, child, (numRows - 1, numCols - 1), ghostSet)
                elif agentBasis == "agent4":
                    path = simA.planWeightedPath(maze, child, (numRows - 1, numCols - 1), ghostSet)
                elif agentBasis == "agent5":
                    path = simA.planWeightedPathVisible(maze, child, (numRows - 1, numCols - 1), ghostSet)
                # print("The path planned by A* is: " + str(path))

                # Resetting timeSteps (an upper bound of 1000) which is used to make sure agent isn't avoiding ghosts forever
                timeSteps = 0

                # Run the agent/ghost game (based on input params)
                while path and not caught and timeSteps < maxSteps:
                    # os.system("clear")

                    timeSteps += 1

                    if simA.doWeReplan(path, simGhosts):

                        if agentBasis == "agent3":
                            path = simA.planPath(maze, (simA.row, simA.col), (numRows - 1, numCols - 1), ghostSet)
                        elif agentBasis == "agent4":
                            path = simA.planWeightedPath(maze, (simA.row, simA.col), (numRows - 1, numCols - 1), ghostSet)
                        elif agentBasis == "agent5":
                            path = simA.planWeightedPathVisible(maze, (simA.row, simA.col), (numRows - 1, numCols - 1), ghostSet)
                        # print("[AGENT 2 SIM " + str(i) + " from " + str(child) + "] Path (post replanning) = " + str(path))
                        if len(path) > 0:
                            nextCell = path.pop(0)
                            # print("[AGENT 2 SIM " + str(i) + " from " + str(child) + "] nextCell (post replanning) = " + str(nextCell))
                            simA.moveAgent(nextCell)
                        elif (simA.row, simA.col) != (numRows - 1, numCols - 1): # If ghosts are blocking all available paths
                            if agentBasis == "agent5":
                                nextCell = simA.stayAwayFromGhosts(maze, simGhosts)
                            else:
                                nextCell = simA.stayAwayFromGhosts(maze, simGhosts)
                            # print("[AGENT 2 SIM " + str(i) + " from " + str(child) + "] nextCell (avoiding ghosts) = " + str(nextCell))
                            simA.moveAgent(nextCell)
                    else: # No replanning required
                        nextCell = path.pop(0)
                        # print("[AGENT 2 SIM " + str(i) + " from " + str(child) + "] Path (no replanning) = " + str(path))
                        simA.moveAgent(nextCell)

                    # End of Moving simA

                    for simGhost in simGhosts:
                        if simGhost.row == simA.row and simGhost.col == simA.col:
                            caught = True
                            break

                    for simGhost in simGhosts:
                        simGhost.moveGhost(maze, numRows, numCols)

                    for simGhost in simGhosts:
                        if simGhost.row == simA.row and simGhost.col == simA.col:
                            caught = True
                            break

                    # End of moving simGhost in simGhosts

                if simA.row == numRows - 1 and a.col == numCols - 1:
                    utilityList.append(1)
                else:
                    utilityList.append(0)
                
                del simA
                del simGhosts
                
            utility[child] = sum(utilityList) / len(utilityList)
            # print(utility[child])

        if utility[child] > maxUtility:
            maxUtility = utility[child]
            bestChild = child

        # print("[AGENT 2 SIM] best child is {bc} and the it's utility is {ut}".format(bc = bestChild, ut = maxUtility))

        if maxUtility > 0.50 and agentBasis == "agent3": # We want to use the maxUtility only if it is worth it
            return bestChild

        if maxUtility > 0 and (agentBasis == "agent4" or agentBasis == "agent5"): # in agents 4 and 5 we don't care, as long as a path exists we'll try
            return bestChild

    # By default return bestChild as current "a" position
    return (a.row, a.col)


# Display for debugging
def dispMaze(maze) -> None:
    for i in range(numRows):
        for j in range(numCols):
            if (maze[i][j] == unBlkd): # Green for 'u'nblocked cells 
                print(Fore.BLACK + str(maze[i][j]), end=" ")
            elif (maze[i][j] == blkd): # Red for 'b'locked cells
                print(Fore.WHITE + str(maze[i][j]), end=" ")
            elif (maze[i][j] == "a"):
                print(Fore.GREEN + str(maze[i][j]), end=" ") 
            else: # For ghosts
                print(Fore.RED + str(maze[i][j]), end=" ")

        print("\n")

numRows= 51
numCols = 51

unBlkd = "u"
blkd = "b"

firstMaze = int(input("Enter the maze number of the first sample in the range: "))
lastMaze = int(input("Enter the maze number of the first sample in the range: "))

maxGhosts = int(input("Enter the max number of ghosts you want to spawn: "))
stepGhosts = int(input("Enter the step size for incrementing number of ghosts: "))
agentNum = int(input("Enter the agent number: "))

totalMazes = lastMaze - firstMaze + 1

chunkSize = math.floor(totalMazes / (maxGhosts / stepGhosts))

tempFirstMaze = 0
tempLastMaze = firstMaze

ghostStart = 0
ghostStart += stepGhosts

init()

# maze = [["_" for _ in range(numCols)] for _ in range(numRows)]
# maze = [[]]
for numGhosts in range(ghostStart, maxGhosts + 1, stepGhosts):

    survivalList = []

    # Determine the max timesteps we will take trying to move the agent
    # It is equivalent to the max number of steps an agent will take per maze run
    maxSteps = 2500 # This was set to 1000 for agents 1 to 3 and updated to 2500 for agent 4 as an improvement

    tempFirstMaze = tempLastMaze + 1

    if numGhosts == ghostStart:
        tempFirstMaze -= 1

    tempLastMaze += chunkSize

    for mazeNo in range(tempFirstMaze, tempLastMaze + 1):

        print("Current Maze Number is {nm} and Number of Ghosts is {ng}".format(nm = mazeNo, ng = numGhosts))
        print(datetime.datetime.now())

        currentMaze = csvops.readCsv(mazeNo, numRows, numCols)
        # print("Maze read from maze" + str(mazeNo) + ".csv is:\n" + str(currentMaze))

        """
        Used tempMaze for visualizing the agent and ghost paths (dynamically and static as well)
        """
        # tempMaze = copy.deepcopy(currentMaze)

        # dispMaze(currentMaze)
        
        # Spawn the ghost(s)
        # For this I may to have take the number of ghosts I am working with and use that to create a list of ghost objects
        # This list will then be used when I want to run the game (like when I need to move the agent and ghosts by steps)
        ghosts = [ghost.Ghost(str(i)) for i in range(numGhosts)]

        ghostSet = set([])

        for g in ghosts:
            g.spawnGhost(currentMaze, numRows, numCols)
            ghostSet.add((g.row, g.col))

        # Spawn the agent
        a = agent.Agent("agent" + str(agentNum))
        # Now compute all the base heuristics for all nodes
        # print("START a.getBaseHeuristics()")
        a.getBaseHeuristics(currentMaze, numRows, numCols)
        # print("FINISHED a.getBaseHeuristics()")

        # Plan a path for the agent
        path = a.planPath(currentMaze, (0, 0), (numRows - 1, numCols - 1), ghostSet)
        # print("The path planned by A* is: " + str(path))

        # By default set the agent as not caught
        caught = False

        # Resetting timeSteps (an upper bound of 1000) which is used to make sure agent isn't avoiding ghosts forever
        timeSteps = 0

        # Run the agent/ghost game (based on input params)
        while path and not caught and (a.row, a.col) != (numRows - 1, numCols - 1) and timeSteps < maxSteps:
            # os.system("clear")

            timeSteps += 1

            if a.name == "agent1":
                nextCell = path.pop(0)
                a.moveAgent(nextCell)
            
            elif a.name == "agent2":
                if a.doWeReplan(path, ghosts):
                    path = a.planPath(currentMaze, (a.row, a.col), (numRows - 1, numCols - 1), ghostSet)
                    # print("[AGENT 2] Path (post replanning) = " + str(path))
                    if len(path) > 0:
                        nextCell = path.pop(0)
                        # print("[AGENT 2] nextCell (post replanning) = " + str(nextCell))
                        a.moveAgent(nextCell)
                    elif (a.row, a.col) != (numRows - 1, numCols - 1): # If ghosts are blocking all available paths
                        nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                        # print("[AGENT 2] nextCell (avoiding ghosts) = " + str(nextCell))
                        a.moveAgent(nextCell)
                else: # No replanning required
                    nextCell = path.pop(0)
                    # print("[AGENT 2] Path (no replanning) = " + str(path))
                    a.moveAgent(nextCell)
            
            elif a.name == "agent3":
                # print("[AGENT 3] Calculate utilities")
                children = findChildren(currentMaze, a, ghosts)
                if children: # if there are any find child with best utility
                    nextCell = monteCarlo(currentMaze, a, children, ghosts, "agent3", maxSteps)
                    # print("[AGENT 3] nextCell (post utility calc) = " + str(nextCell))
                    if nextCell != (a.row, a.col):
                        a.moveAgent(nextCell)
                    else: # Behave exactly like agent 2
                        if a.doWeReplan(path, ghosts):
                            path = a.planPath(currentMaze, (a.row, a.col), (numRows - 1, numCols - 1), ghostSet)
                            # print("[AGENT 2] Path (post replanning) = " + str(path))
                            if len(path) > 0:
                                nextCell = path.pop(0)
                                # print("[AGENT 2] nextCell (post replanning) = " + str(nextCell))
                                a.moveAgent(nextCell)
                            elif (a.row, a.col) != (numRows - 1, numCols - 1): # If ghosts are blocking all available paths
                                nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                                # print("[AGENT 2] nextCell (avoiding ghosts) = " + str(nextCell))
                                a.moveAgent(nextCell)
                        else: # No replanning required
                            nextCell = path.pop(0)
                            # print("[AGENT 2] Path (no replanning) = " + str(path))
                            a.moveAgent(nextCell)
                else: # No children were found
                    nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                    # print("[AGENT 3] nextCell (avoiding ghosts) = " + str(nextCell))
                    a.moveAgent(nextCell)

            elif a.name == "agent4":
                # print("[AGENT 4] Calculate utilities")
                children = findChildren(currentMaze, a, ghosts)
                if children: # if there are any find child with best utility
                    nextCell = monteCarlo(currentMaze, a, children, ghosts, "agent4", maxSteps)
                    # print("[AGENT 4] nextCell (post utility calc) = " + str(nextCell))
                    if nextCell != (a.row, a.col):
                        a.moveAgent(nextCell)
                    else: # Behave exactly like agent 2 BUT WITH WEIGHTED PATH CALCULATION
                        if a.doWeReplan(path, ghosts):
                            path = a.planWeightedPath(currentMaze, (a.row, a.col), (numRows - 1, numCols - 1), ghostSet)
                            # print("[AGENT 4] Path (post replanning) = " + str(path))
                            if len(path) > 0:
                                nextCell = path.pop(0)
                                # print("[AGENT 4] nextCell (post replanning) = " + str(nextCell))
                                a.moveAgent(nextCell)
                            elif (a.row, a.col) != (numRows - 1, numCols - 1): # If ghosts are blocking all available paths
                                nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                                # print("[AGENT 4] nextCell (avoiding ghosts) = " + str(nextCell))
                                a.moveAgent(nextCell)
                        else: # No replanning required
                            nextCell = path.pop(0)
                            # print("[AGENT 4] Path (no replanning) = " + str(path))
                            a.moveAgent(nextCell)
                else: # No children were found
                    nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                    # print("[AGENT 4] nextCell (avoiding ghosts) = " + str(nextCell))
                    a.moveAgent(nextCell)

            elif a.name == "agent5":
                # print("[AGENT 5] Calculate utilities")
                children = findChildren(currentMaze, a, ghosts)
                if children: # if there are any find child with best utility
                    nextCell = monteCarlo(currentMaze, a, children, ghosts, "agent5", maxSteps)
                    # print("[AGENT 5] nextCell (post utility calc) = " + str(nextCell))
                    if nextCell != (a.row, a.col):
                        a.moveAgent(nextCell)
                    else: # Behave exactly like agent 2 BUT WITH WEIGHTED PATH CALCULATION
                        if a.doWeReplan(path, ghosts):
                            path = a.planWeightedPathVisible(currentMaze, (a.row, a.col), (numRows - 1, numCols - 1), ghostSet)
                            # print("[AGENT 5] Path (post replanning) = " + str(path))
                            if len(path) > 0:
                                nextCell = path.pop(0)
                                # print("[AGENT 5] nextCell (post replanning) = " + str(nextCell))
                                a.moveAgent(nextCell)
                            elif (a.row, a.col) != (numRows - 1, numCols - 1): # If ghosts are blocking all available paths
                                nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                                # print("[AGENT 5] nextCell (avoiding ghosts) = " + str(nextCell))
                                a.moveAgent(nextCell)
                        else: # No replanning required
                            nextCell = path.pop(0)
                            # print("[AGENT 5] Path (no replanning) = " + str(path))
                            a.moveAgent(nextCell)
                else: # No children were found
                    nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                    # print("[AGENT 5] nextCell (avoiding ghosts) = " + str(nextCell))
                    a.moveAgent(nextCell)

            else: # Other agents
                pass

            """
            For visualization of agent movement/path
            (1) Make sure to uncomment the initialization of tempMaze above
            (2) Uncomment the below line for displaying agent path
            """
            # tempMaze[a.row][a.col] = "a"

            for g in ghosts:
                if g.row == a.row and g.col == a.col:
                    caught = True
                    break

            ghostSet = set([])

            for g in ghosts:
                g.moveGhost(currentMaze, numRows, numCols)
                ghostSet.add((g.row, g.col))
                
            for g in ghosts:
                if g.row == a.row and g.col == a.col:
                    caught = True
                    break

            """
            For visualization of ghosts movement/paths
            (1) Make sure to uncomment the initialization of tempMaze above
            (2) Uncomment the below line for displaying ghost paths
            """
            # for g in ghosts:
            #     tempMaze[g.row][g.col] = g.name
            
            """
            For a live simulation of agent and ghost movements
            (1) Make sure to uncomment the initialization of tempMaze above
            (2) Uncomment the below lines to display the run second-by-second
            """
            # dispMaze(tempMaze)
            # time.sleep(1)
            # del tempMaze
            # tempMaze = copy.deepcopy(currentMaze)

        # End movement

        """
        For end state diagram of agent and ghost paths throughout the maze
        (1) Make sure to uncomment the initialization of tempMaze and display assignments
        that set the agent and ghosts in tempMaze
        (2) Naturally, also uncomment the below line
        """
        # dispMaze(tempMaze)

        if a.row == numRows - 1 and a.col == numCols - 1:
            print(Fore.BLUE + "We reached the goal!")
            survivalList.append(1)
        else:
            print(Fore.MAGENTA + "The ghost got us :(")
            survivalList.append(0)

    df = pd.DataFrame(survivalList)
    df.columns = ["Survivability"]

    print("agentNum = " + str(agentNum))

    file_name = "./agent_csv/agent" + str(agentNum) + "/Ghost" + str(numGhosts) + '.csv'
    df.to_csv(file_name, encoding='utf-8')
