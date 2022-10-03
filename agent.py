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
        return totalPath[::-1]

    def isValidMove(self, node, maze, closedSet):

        # If we go out of bounds
        if node[0] < 0 or node[1] < 0 or node[0] > 5 or node[1] > 5:
            return False
        
        # If cell is blocked
        if maze[node[0]][node[1]] == "b":
            return False
        
        # If cell is already added to the closedSet
        if closedSet.intersection({node}):
            return False

        # If not none of the above situations arise, the cell can be added!
        return True

    def h(self, current, goal) -> float:
        """
        Heuristic function used here is Euclidian distance
        """
        return math.sqrt(((current[0] - goal[0]) ** 2) + ((current[1] - goal[1]) ** 2))

    def planPath(self, maze, start, goal) -> list:
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

        for i in range(start[0], goal[0] + 1):
            for j in range(start[1], goal[1] + 1):
                # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
                gScore[(i, j)] = infinity # map with default value of Infinity
                # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
                # how cheap a path could be from start to finish if it goes through n.
                fScore[(i, j)] = infinity # map with default value of Infinity

        gScore[start] = 0
        fScore[start] = self.h(start, goal)

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

                if self.isValidMove(neighbor, maze, closedSet):
                    # d(current,neighbor) is the weight of the edge from current to neighbor
                    # tentative_gScore is the distance from start to the neighbor through current
                    gScoreTentative = gScore[current] + 1 # 1 = d(current,neighbor) = step size here
                    if gScoreTentative < gScore[neighbor]:
                        # This path to neighbor is better than any previous one. Record it!
                        cameFrom[neighbor] = current
                        gScore[neighbor] = gScoreTentative
                        fScore[neighbor] = gScoreTentative + self.h(neighbor, goal)
                        if neighbor not in openSet:
                            openSet.append(neighbor)

        # Open set is empty but goal was never reached
        return None
