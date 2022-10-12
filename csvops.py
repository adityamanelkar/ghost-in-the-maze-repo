#!/usr/bin/python
import csv

"""
References:
CSV file creation - https://www.pythontutorial.net/python-basics/python-write-csv-file/

"""

basePath = "./maze_csv"

# Main objective is to convert maze to a .csv file if it is legit
def generateCsv(maze, fileCount):

    with open(basePath + "/maze" + str(fileCount) + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(maze)

# Main objective is to read from an available set of csv files for each iteration of our test
def readCsv(fileCount, numRows, numCols):

    tempMaze = [["_" for _ in range(numCols)] for _ in range(numRows)]

    with open(basePath + "/maze" + str(fileCount) + ".csv", "rt") as f:
        reader = csv.reader(f)
        # for line in reader:
        #     print("line: " + str(line))
        #     list(line)
        i = 0
        for line in reader:
            j = 0
            for item in line:
                tempMaze[i][j] = item.strip()
                # print("tempMaze[" + str(i) + "][" + str(j) + "]: " + str(tempMaze[i][j]))
                j += 1
            i += 1
    
    return tempMaze