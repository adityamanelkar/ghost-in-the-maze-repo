#!/usr/bin/python
import math

# Need to implement some algo for the agent here

# Need to also implement some framework for calling the algo

"""
References:
Pseudo code of A*: https://en.wikipedia.org/wiki/A*_search_algorithm

"""

class Agent():
    """
    Object that has stuff on the agent
    """
    def __init__(self, name) -> None:
        self.name = name
        self.row = self.col = 0
        self.hueristics = {}

    def getBaseHeuristics(self, maze, maxRows, maxCols) -> None:
        """
        This function fetches the actual distance from every cell to the goal
        and stores it in the heuristics dict structure
        """
        if not maze:
            print("Invalid Maze")
            return

        infinity = math.inf

        # First set all the heruistics to infinity by default
        for row in range(maxRows):
            for col in range(maxCols):
                self.hueristics[(row, col)] = infinity
        
        self.hueristics[(maxRows - 1, maxCols - 1)] = 0 # At goal there should be no issues

        for row in range(maxRows):
            for col in range(maxCols):
                if maze[row][col] == "u":
                    self.hueristics[(row, col)] = self.calcHeuristics(maze, (row, col), (maxRows - 1, maxCols - 1))
                    # print("self.hueristics[({r}, {c})] = {value}".format(r = row, c = col, value = self.hueristics[(row, col)]))

        print("self.heuristics was initialized")
        # print(self.hueristics)

    def calcHeuristics(self, maze, start, goal) -> int:
        """
        Uses BD BFS to find the optimal path path from any cell to goal
        """

        if start == goal:
            return 0

        infinity = math.inf

        openSetNorm = [start]
        openSetRev = [goal]
        closedSetNorm = set([])
        closedSetRev = set([])

        # For node n, cameFrom[n] is the node immediately preceding it on the path
        cameFromNorm = {}
        cameFromRev = {}

        xDelta = [0, 1, 0, -1]
        yDelta = [1, 0, -1, 0]

        minDist = infinity
        count = 0
        path = []

        while openSetNorm and openSetRev:
            # print("Closed set Normal\n" + str(closedSetNorm))
            # print("Closed set Reverse\n" + str(closedSetRev))
            
            # Pop current off open list, add to closed list
            currentNorm = openSetNorm.pop(0)
            if not closedSetNorm.intersection({currentNorm}):
                closedSetNorm.add(currentNorm)
            
            currentRev = openSetRev.pop(0)
            if not closedSetRev.intersection({currentRev}):
                closedSetRev.add(currentRev)

            if closedSetNorm.intersection(closedSetRev):
                for elem in closedSetNorm.intersection(closedSetRev):
                    count += 1
                    startLen = len(self.createPathFull(cameFromNorm, elem)) # This returns the path from start to intersection
                    goalLen = len(self.createPathFull(cameFromRev, elem)) # This returns the path from intersection to goal
                    # startToInt.pop()
                    pathLen = startLen + goalLen + 1
                    if pathLen < minDist:
                        minDist = pathLen

                if count > 0:
                    return minDist

            for i in range(4):

                neighborNorm = (currentNorm[0] + xDelta[i], currentNorm[1] + yDelta[i])

                if self.isValidMove(neighborNorm, maze, closedSetNorm):
                    cameFromNorm[neighborNorm] = currentNorm
                    if neighborNorm not in openSetNorm:
                        openSetNorm.append(neighborNorm)
                    if not closedSetNorm.intersection({neighborNorm}):
                        closedSetNorm.add(neighborNorm)
                
                neighborRev = (currentRev[0] + xDelta[i], currentRev[1] + yDelta[i])

                if self.isValidMove(neighborRev, maze, closedSetRev):
                    cameFromRev[neighborRev] = currentRev
                    if neighborRev not in openSetRev:
                        openSetRev.append(neighborRev)
                    if not closedSetRev.intersection({neighborRev }):
                        closedSetRev.add(neighborRev)

        return infinity # If goal was never reached

    def moveAgent(self, cell=None) -> None:
        if not cell:
            return
        else:
            (self.row, self.col) = cell

    def createPath(self, cameFrom, current):
        totalPath = [current]
        while current in cameFrom:
            current = cameFrom[current]
            totalPath.append(current)
        actualPath = totalPath[::-1]
        actualPath.pop(0)
        return actualPath

    def createPathFull(self, cameFrom, current):
        totalPath = [current]
        while current in cameFrom:
            current = cameFrom[current]
            totalPath.append(current)
        return totalPath[::-1]

    def isValidMove(self, node, maze, closedSet, ghostSet=set([])):

        # If we go out of bounds
        if node[0] < 0 or node[1] < 0 or node[0] >= len(maze) or node[1] >= len(maze[0]):
            return False
            
        # If cell is blocked
        if maze[node[0]][node[1]] == "b":
            return False
        
        # If cell is already added to the closedSet
        if closedSet.intersection({node}):
            return False
        
        if ghostSet.intersection({node}):
            return False

        # If not none of the above situations arise, the cell can be added!
        return True

    def hManhattan(self, current, goal) -> int:
        """
        Heuristic function used here is Manhattan distance - ! not used
        """
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def hEuclidian(self, current, goal) -> float:
        """
        Heuristic function used here is Euclidian distance - ! not used
        """
        return math.sqrt(((current[0] - goal[0]) ** 2) + ((current[1] - goal[1]) ** 2))

    def planPath(self, maze, start, goal, ghostSet) -> list:
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        openSet = [start]
        closedSet = set([])
        infinity = math.inf

        # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
        # to n currently known.
        cameFrom = {}
        gScore = {}
        fScore = {}

        xDelta = [0, 1, 0, -1]
        yDelta = [1, 0, -1, 0]

        for i in range(goal[0] + 1):
            for j in range(goal[1] + 1):
                # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
                gScore[(i, j)] = infinity # map with default value of Infinity
                # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
                # how cheap a path could be from start to finish if it goes through n.
                fScore[(i, j)] = infinity # map with default value of Infinity

        gScore[start] = 0
        fScore[start] = self.hueristics[start]

        while openSet:
            # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
            # current := the node in openSet having the lowest fScore[] value !!!!!

            # Get the current node
            current = openSet[0]
            curIdx = 0

            for idx, item in enumerate(openSet):
                if fScore[item] < fScore[current]:
                    current = item
                    curIdx = idx

            # Pop current off open list, add to closed list
            current = openSet.pop(curIdx)
            closedSet.add(current)

            if current == goal:
                return self.createPath(cameFrom, current) # This returns the best path found through a*

            for i in range(4):
                neighbor = (current[0] + xDelta[i], current[1] + yDelta[i])

                if self.isValidMove(neighbor, maze, closedSet, ghostSet):
                    # d(current,neighbor) is the weight of the edge from current to neighbor
                    # tentative_gScore is the distance from start to the neighbor through current
                    gScoreTentative = gScore[current] + 1 # 1 = d(current,neighbor) = step size here
                    if gScoreTentative < gScore[neighbor]:
                        # This path to neighbor is better than any previous one. Record it!
                        cameFrom[neighbor] = current
                        gScore[neighbor] = gScoreTentative
                        fScore[neighbor] = gScoreTentative + self.hueristics[neighbor]
                        if neighbor not in openSet:
                            openSet.append(neighbor)

        # Open set is empty but goal was never reached
        return []

    def calcStepWeight(self, maze, node, ghostSet, invisibleCheck="False") -> int:
        """
        Here we want to add different wights so that certain cells around the ghost are
        generally discouraged/penalized (but not completely blocked out)

        As a part of agent 4 changes, we believe that this will help get better paths
        (which are not optimal, but which would generally help reduce replanning)

        For starters, we want to increase the weight of cells diagonally around ghosts
        to weights of "2" or more and those in horizontal and vertical cells around ghosts to
        weights of "3" or more. These will be used instead of the existing default weight of "1"

        For agent 5 specifically, invisibleCheck would be set to true - so now the ghosts in walls
        will just be skipped altogether
        """

        straightX = [0, 1, 0, -1]
        straightY = [1, 0, -1, 0]

        diagonalX = [1, -1, 1, -1]
        diagonalY = [1, 1, -1, -1]

        weight = 1 # Default weight

        for g in ghostSet:

            # For agent 5 if the ghost is in a blocked cell then we don't wanna check for weights
            if invisibleCheck and maze[g[0]][g[1]] == "b":
                continue

            for i in range(4):

                # Add an additional penalty weight 4
                if node == (g[0] + straightX[i], g[1] + straightY[i]):
                    weight += 2

                # Add an additional penalty weight 2
                if node == (g[0] + diagonalX[i], g[1] + diagonalY[i]):
                    weight += 1

        # Return the cumulative weight
        return weight

    def planWeightedPathVisible(self, maze, start, goal, ghostSet) -> list:
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        openSet = [start]
        closedSet = set([])
        infinity = math.inf

        # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
        # to n currently known.
        cameFrom = {}
        gScore = {}
        fScore = {}

        xDelta = [0, 1, 0, -1]
        yDelta = [1, 0, -1, 0]

        for i in range(goal[0] + 1):
            for j in range(goal[1] + 1):
                # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
                gScore[(i, j)] = infinity # map with default value of Infinity
                # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
                # how cheap a path could be from start to finish if it goes through n.
                fScore[(i, j)] = infinity # map with default value of Infinity

        gScore[start] = 0
        fScore[start] = self.hueristics[start]

        while openSet:
            # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
            # current := the node in openSet having the lowest fScore[] value !!!!!

            # Get the current node
            current = openSet[0]
            curIdx = 0

            for idx, item in enumerate(openSet):
                if fScore[item] < fScore[current]:
                    current = item
                    curIdx = idx

            # Pop current off open list, add to closed list
            current = openSet.pop(curIdx)
            closedSet.add(current)

            if current == goal:
                return self.createPath(cameFrom, current) # This returns the best path found through a*

            for i in range(4):
                neighbor = (current[0] + xDelta[i], current[1] + yDelta[i])

                if self.isValidMove(neighbor, maze, closedSet, ghostSet):
                    # d(current,neighbor) is the weight of the edge from current to neighbor
                    # tentative_gScore is the distance from start to the neighbor through current
                    gScoreTentative = gScore[current] + self.calcStepWeight(maze, neighbor, ghostSet, invisibleCheck="True") # 1 = d(current,neighbor) = default step size here
                    if gScoreTentative < gScore[neighbor]:
                        # This path to neighbor is better than any previous one. Record it!
                        cameFrom[neighbor] = current
                        gScore[neighbor] = gScoreTentative
                        fScore[neighbor] = gScoreTentative + self.hueristics[neighbor]
                        if neighbor not in openSet:
                            openSet.append(neighbor)

        # Open set is empty but goal was never reached
        return []

    def planWeightedPath(self, maze, start, goal, ghostSet) -> list:
        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        openSet = [start]
        closedSet = set([])
        infinity = math.inf

        # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
        # to n currently known.
        cameFrom = {}
        gScore = {}
        fScore = {}

        xDelta = [0, 1, 0, -1]
        yDelta = [1, 0, -1, 0]

        for i in range(goal[0] + 1):
            for j in range(goal[1] + 1):
                # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
                gScore[(i, j)] = infinity # map with default value of Infinity
                # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
                # how cheap a path could be from start to finish if it goes through n.
                fScore[(i, j)] = infinity # map with default value of Infinity

        gScore[start] = 0
        fScore[start] = self.hueristics[start]

        while openSet:
            # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
            # current := the node in openSet having the lowest fScore[] value !!!!!

            # Get the current node
            current = openSet[0]
            curIdx = 0

            for idx, item in enumerate(openSet):
                if fScore[item] < fScore[current]:
                    current = item
                    curIdx = idx

            # Pop current off open list, add to closed list
            current = openSet.pop(curIdx)
            closedSet.add(current)

            if current == goal:
                return self.createPath(cameFrom, current) # This returns the best path found through a*

            for i in range(4):
                neighbor = (current[0] + xDelta[i], current[1] + yDelta[i])

                if self.isValidMove(neighbor, maze, closedSet, ghostSet):
                    # d(current,neighbor) is the weight of the edge from current to neighbor
                    # tentative_gScore is the distance from start to the neighbor through current
                    gScoreTentative = gScore[current] + self.calcStepWeight(maze, neighbor, ghostSet) # 1 = d(current,neighbor) = default step size here
                    if gScoreTentative < gScore[neighbor]:
                        # This path to neighbor is better than any previous one. Record it!
                        cameFrom[neighbor] = current
                        gScore[neighbor] = gScoreTentative
                        fScore[neighbor] = gScoreTentative + self.hueristics[neighbor]
                        if neighbor not in openSet:
                            openSet.append(neighbor)

        # Open set is empty but goal was never reached
        return []

    def stayAwayFromGhosts(self, currentMaze, ghosts) -> tuple:

        infinity = math.inf

        xDelta = [0, 1, 0, -1]
        yDelta = [1, 0, -1, 0]

        minDist = infinity
        neighborDist = infinity

        # Calculate which visisble ghost is the closest
        for ghost in ghosts:
            if currentMaze[ghost.row][ghost.col] == "u":
                tempDist = min(minDist, self.hEuclidian((self.row, self.col), (ghost.row, ghost.col)))
                if tempDist != minDist:
                    gCloseRow, gCloseCol = ghost.row, ghost.col
                    minDist = tempDist
        
        # We wanna have a default case where the agent stays in the same spot if there are no better moves
        bestNeighbor = (self.row, self.col)
        breakCnt = 0

        for i in range(4):
            neighbor = (self.row + xDelta[i], self.col + yDelta[i])
            # If we go out of bounds
            if neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] >= len(currentMaze) or neighbor[1] >= len(currentMaze[0]):
                breakCnt += 1
                continue
                
            # If cell is blocked
            if currentMaze[neighbor[0]][neighbor[1]] == "b":
                breakCnt += 1
                continue

            # If cell has a ghost
            for ghost in ghosts:
                if neighbor == (ghost.row, ghost.col):
                    breakCnt += 1
                    break
            
            if breakCnt == 0:
                tempNeighborDist = min(neighborDist, self.hManhattan(neighbor, (gCloseRow, gCloseCol)))

                if neighborDist != tempNeighborDist:
                    bestNeighbor = neighbor
            else: # Reset the counter
                breakCnt = 0

        return bestNeighbor

    def doWeReplan(self, path, ghosts) -> bool:

        for ghost in ghosts:
            if (ghost.row, ghost.col) in path:
                return True

        return False