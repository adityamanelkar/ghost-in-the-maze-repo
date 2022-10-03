#!/usr/bin/python
import random
import bdbfs

# This code would have all the necessary setup for spawning the ghost(s)

class Ghost:

    def __init__(self, name) -> None:
        self.name = name # typically will be something like "1", "2", etc.
        self.row = 0
        self.col = 0

    # Need to make sure the ghost is spawned in a cell that is not walled off (i.e. it lies in one of the solution paths for the agent)
    def spawnGhost(self, maze, maxRows, maxCols) -> None:

        legitSpawn = False

        while not legitSpawn:

            closedList = []
            closedList = set(closedList)

            # First select a random cell from the lot to spawn into
            row = random.randint(0, maxRows - 1)
            col = random.randint(0, maxCols - 1)

            # We do not want to waste time re-checking old spawn co-ordinates
            if closedList.intersection({(row, col)}):
                continue

            # If cell is blocked, try again till you get an unblocked cell
            if maze[row][col] == "b":
                continue

            # We do not want to spawn at the start
            if row == 0 and col == 0:
                continue

            # Once you get an unblocked cell, check if that cell is reachable from START
            # If it is, then set it as the spawn location of the ghost
            # I'm re-using the BDBFS code here to check if the start and spawn point have a path
            if bdbfs.enterTheDragon(maze, maxRows, maxCols, (row, col)):
                self.row = row
                self.col = col
                legitSpawn = True

            else: # the spawn co-ordinate was not reachable from START
                closedList.add((row, col))

            # We just loop and try again if legitSpawn = False
    
    def isValidMove(self, maze, row, col, maxRows, maxCols) -> bool:
        
        # Ghost cannot move outside the maze
        if row < 0 or col < 0 or row >= maxRows or col >= maxCols:
            return False

        # If the cell the ghost is about to move into is blocked
        if maze[row][col] == "b":
            if random.random() <= 0.5: # We want the ghost to stay in the same spot 50% of the time
                return False

        # If not none of the above situations arise, the cell can be added!
        return True

    def moveGhost(self, maze, maxRows, maxCols) -> None:
        
        # Here I need to allow for ghosts to move in all four directions
        # Constraints: Ghost can move into a "b"locked cell, but it does so with 0.5 probability or stays in the same cell
        # I'm guessing here, but I think ghost should have a random AI (i.e. it is not an adversary)
        
        chanceFactor = random.random()

        rowNew = self.row
        colNew = self.col

        if chanceFactor <= 0.25:
            rowNew += 1
        
        elif chanceFactor <= 0.5:
            colNew += 1
        
        elif chanceFactor <= 0.75:
            rowNew -= 1
        
        else: # chanceFactor between 0.75 and 1
            colNew -= 1

        # Check if the new move is valid
        if self.isValidMove(maze, rowNew, colNew, maxRows, maxCols):
            self.row = rowNew
            self.col = colNew
