#!/usr/bin/python
import csvops

"""
References:


"""
numRows= 6
numCols = 6

# maze = [["_" for _ in range(numCols)] for _ in range(numRows)]
maze = [[]]

mainMaze = csvops.readCsv(1, numRows, numCols)
print("Maze read from maze1.csv is:\n" + str(mainMaze))