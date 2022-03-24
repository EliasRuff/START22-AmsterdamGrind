import sklearn.cluster as sk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



randomDate = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=[
        "metMinutes",
        "timeStart",
        "duration",
        "age"
    ])

pandaMove = pd.read_json("./movedata.json")
pandaActivity = pd.read_json("./activities.json")

def timeToInt(time):
    hours = (time.split(":")[0])[:-1]
    minutes = time.split(":")[1]
    timeInt = int(minutes) + 60*int(hours)
    return timeInt

def genderToInt(gender):
    if(gender == "female"):
        return 0
    else:
        return 1

pandaMove["timeStart"] = pandaMove["timeStart"].map(lambda x: timeToInt(str(x)[-5:]))
pandasAgeGenderOnly = pandaActivity[["userId","age", "gender"]]
pandasAgeGenderOnly["gender"] = pandasAgeGenderOnly["gender"].map(lambda x: genderToInt(str(x)))
pandasAgeGenderOnly = pandasAgeGenderOnly.drop_duplicates()

conncatinated = pd.merge(left = pandaMove, right= pandasAgeGenderOnly, how="inner")
conncatinated["intensity"] = conncatinated["duration"] * conncatinated["metMinutes"]
#print(conncatinated)


#remove userId for clustering
tracker_data = conncatinated[
    [
        "metMinutes",
        "timeStart",
        "duration",
        "age",
        "gender",
        "intensity"
    ]
].values


#Cluster the data and find best k (cluster Amount)

SquaredDistancesPerK = []

for k in range(1, 15):
    kmeans = sk.KMeans(n_clusters = k).fit(tracker_data)
    SquaredDistancesPerK.append(kmeans.inertia_)

#Plot
plt.plot(range(1,15), SquaredDistancesPerK, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k with Gender & Intensity')
plt.show()