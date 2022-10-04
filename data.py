#!/usr/bin/python
import matplotlib.pyplot as plt
import pandas as pd

def ploting (Agent_data):
    x = [i+1 for i in range(len(Agent_data)) ]
    y = Agent_data
    plt.plot(x, y, marker='o', color='r')
    plt.xticks(x)
    plt.xlabel('No. of Ghosts')
    plt.ylabel('Agent_Survivablity')
    plt.title("Survivability vs Ghost Density")
    plt.show()

Agent_data = []

Agent_No = int(input("Enter Agent No.: "))
no_of_ghost = int(input("Enter the Range No. of Ghosts: "))

for i in range(1, no_of_ghost + 1):
    filepath = "./agent_csv/agent" + str(Agent_No) + "/Ghost" + str(i) + ".csv"
    df = pd.read_csv(filepath)
    avg_survivability = df["Survivability"].mean()
    Agent_data.append(avg_survivability)

ploting(Agent_data)
