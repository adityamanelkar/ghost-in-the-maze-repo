#!/usr/bin/python
from collections import deque
from queue import Empty

"""
References:
general BFS implementation - https://www.geeksforgeeks.org/breadth-first-traversal-bfs-on-a-2d-array/

"""

# Check if any common cells exist in the sets of visited cells in either direction
def isCommonCellAvaialable():
    if visitedSetStart.intersection(visitedSetGoal):
        # print("A common child was found in both BFS directions!")
        return True
    else:
        # print("No common child was found yet :(")
        return False

# Check if cell to be added as a child is indeed a valid one
def isValidCell(maze, row, col, dir="start-goal"):
    
    # If we go out of bounds
    if row < 0 or col < 0 or row >= maxRows or col >= maxCols:
        return False
    
    # If cell is blocked
    if maze[row][col] == "b":
        return False
    
    # If cell is already added to visited cells set
    if dir == "start-goal":
        if visitedSetStart.intersection({(row, col)}):
            return False
    else: # goal-start
        if visitedSetGoal.intersection({(row, col)}):
            return False

    # If not none of the above situations arise, the cell can be added!
    return True

# Our main BD BFS function
def doesPathExist(maze, lastCell):

    # Queues to keep track of the BFS
    queueStart = deque()
    queueGoal = deque()

    # Lists to later help with deciding children in BFS
    deltaRowStart = [0, 1, 0, -1]
    deltaColStart = [1, 0, -1, 0]

    deltaRowGoal = [0, 1, 0, -1]
    deltaColGoal = [1, 0, -1, 0]

    ####################
    # For START -> GOAL
    ####################
    # Append the start cell coordinates to the queue
    queueStart.append((0, 0))

    # Then make sure we are marking the start point as visited
    # visitedMatrixStart[0][0] = True
    visitedSetStart.add((0, 0))

    ####################
    # For GOAL -> START
    ####################
    # Append the start cell coordinates to the queue
    queueGoal.append((lastCell[0], lastCell[1]))

    # Then make sure we are marking the start point as visited
    # visitedMatrixGoal[maxRows - 1][maxCols -1] = True
    visitedSetGoal.add((lastCell[0], lastCell[1]))

    # We want to continue checking until we have
    # (1) Checked all children from either side OR
    # (2) Reached a common cell
    while queueStart and queueGoal:
        
        # START -> GOAL
        parentStart = queueStart.popleft()
        xStart = parentStart[0]
        yStart = parentStart[1]

        # print("xStart = " + str(xStart) + " yStart = " + str(yStart) + "\n")

        for i in range(4): # I have to check all direction children (moving towrds GOAL) *
            xChildStart = xStart + deltaRowStart[i]
            yChildStart = yStart + deltaColStart[i]

            if isValidCell(maze, xChildStart, yChildStart, "start-goal"):
                queueStart.append((xChildStart, yChildStart))
                # visitedMatrixStart[xChildStart][yChildStart] = True
                visitedSetStart.add((xChildStart, yChildStart))

        # GOAL -> START
        parentGoal = queueGoal.popleft()
        xGoal = parentGoal[0]
        yGoal = parentGoal[1]

        # print("xGoal = " + str(xGoal) + " yGoal = " + str(yGoal) + "\n")

        for i in range(4): # I have to check all direction children (moving towards START) *
            xChildGoal = xGoal + deltaRowGoal[i]
            yChildGoal = yGoal + deltaColGoal[i]

            if isValidCell(maze, xChildGoal, yChildGoal, "goal-start"):
                queueGoal.append((xChildGoal, yChildGoal))
                # visitedMatrixGoal[xChildGoal][yChildGoal] = True
                visitedSetGoal.add((xChildGoal, yChildGoal))

        if isCommonCellAvaialable():
            return True
    
    # At least one of the directions must have hit a wall
    return False

# This will be the entry point from maze.py
def enterTheDragon(maze, numRows, numCols, lastCell):
    
    # Some initializations
    # global visitedMatrixStart
    # global visitedMatrixGoal
    global visitedSetStart
    global visitedSetGoal
    global maxRows, maxCols

    maxRows = numRows
    maxCols = numCols

    if not maze:
        print("The maze is empty!")
        return False

    if numRows <= 0 or numCols <= 0:
        print("A non-positive number of rows or columns was passed!")
        return False

    # visitedMatrixStart = [[False for _ in range(numCols)] for _ in range(numRows)] # Will indicate to us which cells have been visited
    # visitedMatrixGoal = [[False for _ in range(numCols)] for _ in range(numRows)] # Will indicate to us which cells have been visited

    visitedSetStart = []
    visitedSetStart = set(visitedSetStart)

    visitedSetGoal = []
    visitedSetGoal = set(visitedSetGoal)

    # Do a BD BFS from START -> GOAL and simultaneously from GOAL -> START
    if doesPathExist(maze, lastCell):
        # print("A path exists, so one can reach the goal from the start!")
        return True
    else:
        # print("Sadly one cannot span the maze :(")
        return False

"""
* I initially thought I would need to only check for distances towards the GOAL (bottom-right) or START (top-left) when initializing the BFS from START and GOAL respectively.
  I soon realized that it was not the best way of going about things, coz my one of my queues would run out and I'd exit.

"""