import matplotlib.pyplot as plt
import pandas as pd

star_agent =  int(input("Enter the first agent number: "))
end_agent = int(input("Enter the last agent number: "))
No_of_Ghosts = int(input("Enter the number of ghosts that you want to compare data for: "))


agent_nums = end_agent-star_agent + 1

#List that contains the final survivability of the agents for the particular number of ghosts
Agent_data = []

#Traverse to the data files of particular agents and their respective no of ghost files
for j in range(star_agent,(end_agent)+1):
    filepath = "./agent_csv/agent" + str(j) + "/Ghost" + str(No_of_Ghosts) + ".csv"
    df = pd.read_csv(filepath)
    avg_survivability = round(df["Survivability"].mean(),2)
    Agent_data.append(avg_survivability)


#X axis of graph = Agents we need to compare
x = [i for i in range(star_agent,(end_agent)+1)]

# Plotting the bar graph between Agents and their survivability for the particular number of ghosts
plt.bar(x, Agent_data, color ='indianred',width = 0.4)
plt.xlabel("Agents")
plt.xticks(x)
plt.ylabel("Survivability")
plt.title("Number of Ghosts: "+str(No_of_Ghosts))
plt.show()