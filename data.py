#!/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd

def ploting (Agent_data, ghostStart, maxGhosts, stepGhosts):
    x = [i for i in range(ghostStart, maxGhosts + 1, stepGhosts)]
    y = Agent_data
    plt.plot(x, y, marker='o', color='r')
    plt.xticks(x)
    for i, j in zip(x, y):
        plt.text(i, j + 0.005, "({}, {})".format(i, round(j, 2)))
    plt.xlabel('No. of Ghosts')
    plt.ylabel('Agent_Survivablity')
    plt.title("Survivability vs Ghost Density")
    plt.show()

Agent_data = []

agentNum = int(input("Enter the agent number: "))
maxGhosts = int(input("Enter the max number of ghosts that you want to cram data for: "))
stepGhosts = int(input("Enter the step size for increamenting number of ghosts: "))
ghostStart = 0
ghostStart += stepGhosts

for i in range(ghostStart, maxGhosts + 1, stepGhosts):
    filepath = "./agent_csv/agent" + str(agentNum) + "/Ghost" + str(i) + ".csv"
    df = pd.read_csv(filepath)
    avg_survivability = df["Survivability"].mean()
    Agent_data.append(avg_survivability)

ploting(Agent_data, ghostStart, maxGhosts, stepGhosts)
