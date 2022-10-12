#!/usr/bin/python
import csvops
import time
import os
import math
import copy
from colorama import init
from colorama import Fore
import agent
import ghost
import pandas as pd
import concurrent.futures as futures
from traceback import print_exc

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
        if maze[child[0]][child[1]] == "b":
            continue

        # If not none of the above situations arise, the cell can be added!
        for ghost in ghosts:
            if child == (ghost.row, ghost.col):
                breakCnt += 1
                break
        
        if breakCnt == 0:
            children.append(child)

    return children

# Find utility values for children
def findUtility(iteration, child, simA, simGhosts, maze, numRows, numCols):
    """
    Finds the utility value (either 0 or 1 indicating the simulation survived or not)
    """
    # By default set the agent as not caught
    caught = False

    for simGhost in simGhosts:
        if simGhost.row == simA.row and simGhost.col == simA.col:
            caught = True

    # Plan a path for the agent
    path = simA.planPath(maze, child, (numRows - 1, numCols - 1))
    # print("The path planned by A* is: " + str(path))

    # Resetting timeSteps (an upper bound of 1000) which is used to make sure agent isn't avoiding ghosts forever
    timeSteps = 0

    # Run the agent/ghost game (based on input params)
    while path and not caught and timeSteps < 1000 and (simA.row <= numRows - 1 and simA.col <= numCols - 1):
        # os.system("clear")

        timeSteps += 1

        if simA.doWeReplan(path, simGhosts):
            path = simA.planPath(maze, (simA.row, simA.col), (numRows - 1, numCols - 1))
            # print("[AGENT 2 SIM " + str(i) + " from " + str(child) + "] Path (post replanning) = " + str(path))
            if len(path) > 0:
                nextCell = path.pop(0)
                # print("[AGENT 2 SIM " + str(i) + " from " + str(child) + "] nextCell (post replanning) = " + str(nextCell))
                simA.moveAgent(nextCell)
            elif (simA.row, simA.col) != (numRows - 1, numCols - 1): # If ghosts are blocking all available paths
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

    if simA.row == numRows - 1 and simA.col == numCols - 1 and not caught:
        print("Returning utility value [1] for sim: " + str(iteration))
        del simA
        del simGhosts
        return 1
    else:
        print("Returning utility value [0] for sim: " + str(iteration))
        del simA
        del simGhosts
        return 0


# Pick children with best utility values
def monteCarlo(maze, a, children, gs, agentBasis="agent2") -> tuple:
    """
    Compare utilities for each of the children of a and return the coordinates of the child w/ highest utility
    """
    import ghost

    # Map with utility values (asked Aravind and he said it was better to recalculate it - so didn't make it global)
    avgUtility = {}

    numRows = len(maze)
    numCols = len(maze[0])

    bestChild = (a.row, a.col)
    maxUtility = 0
    iterList = []

    numSims = 100

    # I want to run [numSims] sims at the moment to calculate average utilities
    for i in range(numSims):
        iterList.append(i)

    if agentBasis == "agent2":
        
        for child in children:

            simA = copy.deepcopy(a)

            (simA.row, simA.col) = child # Make sure our current simulation starts with current child

            simGhosts = [ghost.Ghost(str(i)) for i in range(len(gs))]

            for simGhost, g in zip(simGhosts, gs):
                simGhost = copy.deepcopy(g)
            
            for simGhost in simGhosts:
                    simGhost.moveGhost(maze, numRows, numCols) # Simulate moving the ghosts once as wel

            utilityList = []

            childList = [child] * numSims
            aList = [simA] * numSims
            gsList = [simGhosts] * numSims
            mazeList = [maze] * numSims
            rowsList = [numRows] * numSims
            colsList = [numCols] * numSims

            with futures.ProcessPoolExecutor(max_workers=os.cpu_count() - 2) as executor:
                # for utility in executor.map(findUtility, childList, aList, gsList, mazeList, rowsList, colsList):
                #     # print('The utility: %s' % (utility))
                #     utilityList.append(utility)

                # Different approach I found on stackoverflow (https://stackoverflow.com/a/42096963/5722359)
                futuresRet = executor.map(findUtility, iterList, childList, aList, gsList, mazeList, rowsList, colsList)
                print("Waiting for furtureList to finish computing")

            print("futureList ready!")
            utilityList = list(futuresRet)

            # for futureVal in futureList:
            #     print("type(futureVal) = ", type(futureVal))
            #     try:
            #         utilityList.append(futureVal)
            #     except:
            #         print_exc()

            print("Length of utilityList is: ")
            print(len(utilityList))

            print("For child {c} the utility list is {utl}".format(c = child, utl = utilityList))

            avgUtility[child] = sum(utilityList) / len(utilityList)
            # print(utility[child])

            if avgUtility[child] > maxUtility:
                maxUtility = avgUtility[child]
                bestChild = child

        # print("[AGENT 2 SIM] best child is {bc} and the it's utility is {ut}".format(bc = bestChild, ut = maxUtility))

        if maxUtility > 0.15: # We want to use the maxUtility only if it is worth it
            return bestChild

    # if agentBasis is not agent2 then return bestChild as current a position
    return (a.row, a.col)


# Display for debugging
def dispMaze(maze) -> None:
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

if __name__ == "__main__":

    numRows= 51
    numCols = 51

    unBlkd = "u"
    blkd = "b"

    firstMaze = int(input("Enter the maze number of the first sample in the range: "))
    lastMaze = int(input("Enter the maze number of the last sample in the range: "))

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

        tempFirstMaze = tempLastMaze + 1

        if numGhosts == ghostStart:
            tempFirstMaze -= 1

        tempLastMaze += chunkSize

        for mazeNo in range(tempFirstMaze, tempLastMaze + 1):

            print("Current Maze Number is {nm} and Number of Ghosts is {ng}".format(nm = mazeNo, ng = numGhosts))

            currentMaze = csvops.readCsv(mazeNo, numRows, numCols)
            # print("Maze read from maze" + str(mazeNo) + ".csv is:\n" + str(currentMaze))

            # dispMaze(currentMaze)
            
            # Spawn the ghost(s)
            # For this I may to have take the number of ghosts I am working with and use that to create a list of ghost objects
            # This list will then be used when I want to run the game (like when I need to move the agent and ghosts by steps)
            ghosts = [ghost.Ghost(str(i)) for i in range(numGhosts)]

            for g in ghosts:
                g.spawnGhost(currentMaze, numRows, numCols)

            # Spawn the agent
            a = agent.Agent("agent" + str(agentNum))
            # Now compute all the base heuristics for all nodes
            # print("START a.getBaseHeuristics()")
            a.getBaseHeuristics(currentMaze, numRows, numCols)
            # print("FINISHED a.getBaseHeuristics()")

            # Plan a path for the agent
            path = a.planPath(currentMaze, (0, 0), (numRows - 1, numCols - 1))
            # print("The path planned by A* is: " + str(path))

            # By default set the agent as not caught
            caught = False

            # Resetting timeSteps (an upper bound of 1000) which is used to make sure agent isn't avoiding ghosts forever
            timeSteps = 0

            # Run the agent/ghost game (based on input params)
            while path and not caught and (a.row, a.col) != (numRows - 1, numCols - 1) and timeSteps < 1001:
                # os.system("clear")

                timeSteps += 1

                if a.name == "agent1":
                    nextCell = path.pop(0)
                    a.moveAgent(nextCell)
                
                elif a.name == "agent2":
                    if a.doWeReplan(path, ghosts):
                        path = a.planPath(currentMaze, (a.row, a.col), (numRows - 1, numCols - 1))
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
                    print("[AGENT 3] Calculate utilities")
                    children = findChildren(currentMaze, a, ghosts)
                    if children: # if there are any find child with best utility
                        nextCell = monteCarlo(currentMaze, a, children, ghosts, agentBasis="agent2")
                        print("[AGENT 3] nextCell (post utility calc) = " + str(nextCell))
                        if nextCell != (a.row, a.col):
                            a.moveAgent(nextCell)
                        else: # Behave exactly like agent 2
                            if a.doWeReplan(path, ghosts):
                                path = a.planPath(currentMaze, (a.row, a.col), (numRows - 1, numCols - 1))
                                print("[AGENT 2] Path (post replanning) = " + str(path))
                                if len(path) > 0:
                                    nextCell = path.pop(0)
                                    print("[AGENT 2] nextCell (post replanning) = " + str(nextCell))
                                    a.moveAgent(nextCell)
                                elif (a.row, a.col) != (numRows - 1, numCols - 1): # If ghosts are blocking all available paths
                                    nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                                    print("[AGENT 2] nextCell (avoiding ghosts) = " + str(nextCell))
                                    a.moveAgent(nextCell)
                            else: # No replanning required
                                nextCell = path.pop(0)
                                print("[AGENT 2] Path (no replanning) = " + str(path))
                                a.moveAgent(nextCell)
                    else: # No children were found
                        nextCell = a.stayAwayFromGhosts(currentMaze, ghosts)
                        print("[AGENT 3] nextCell (avoiding ghosts) = " + str(nextCell))
                        a.moveAgent(nextCell)

                else: # Other agents
                    pass

                # currentMaze[a.row][a.col] = "a"

                for g in ghosts:
                    if g.row == a.row and g.col == a.col:
                        caught = True
                        break

                for g in ghosts:
                    g.moveGhost(currentMaze, numRows, numCols)

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
