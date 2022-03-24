import sklearn.cluster as sk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

np.random.seed(1337)

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
def defaultValue():
    return [0,0,0,0,0,0]



def init(pandaActivity, pandaMove):
    userBelongings = defaultdict(lambda: [0,0,0,0,0,0])
    pandaMove["timeStart"] = pandaMove["timeStart"].map(lambda x: timeToInt(str(x)[-5:]))
    pandasAgeGenderOnly = pandaActivity[["userId","age", "gender"]]
    pandasAgeGenderOnly["gender"] = pandasAgeGenderOnly["gender"].map(lambda x: genderToInt(str(x)))
    pandasAgeGenderOnly = pandasAgeGenderOnly.drop_duplicates()

    conncatinated = pd.merge(left = pandaMove, right= pandasAgeGenderOnly, how="inner")
    conncatinated["intensity"] = conncatinated["duration"] * conncatinated["metMinutes"]

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
    kmeans = sk.KMeans(n_clusters = 6).fit(tracker_data)

    #After clustering add cluster column to original data (which still includes userId)
    labels = kmeans.labels_
    conncatinated["cluster"] = labels

    #get cluster distributions for users
    EntriesPerUserId = conncatinated.groupby(['userId'])

    ClusterEntriesPerUserId = conncatinated.groupby(['userId','cluster'])

    userIds = conncatinated["userId"].drop_duplicates()

    for id in userIds:
        userBelongings[id] = [0,0,0,0,0,0]

    for userId, group in ClusterEntriesPerUserId:
        id = userId[0]
        cluster = userId[1]
        size = len(group.index)
        userBelongings[id][cluster] += size

    for userId, group in EntriesPerUserId:
        size = len(group.index)
        for i in range(0,6):
            userBelongings[userId][i] /=size

    #createPlots(kmeans=kmeans)
    return userBelongings


def createPlots(kmeans):
    metMinutes = [kmeans.cluster_centers_[k][0] for k in range(len(kmeans.cluster_centers_))]
    timeStart = [kmeans.cluster_centers_[k][1] for k in range(len(kmeans.cluster_centers_))]
    duration = [kmeans.cluster_centers_[k][2] for k in range(len(kmeans.cluster_centers_))]
    age = [kmeans.cluster_centers_[k][3] for k in range(len(kmeans.cluster_centers_))]
    gender = [kmeans.cluster_centers_[k][4] for k in range(len(kmeans.cluster_centers_))]
    clusterIntensities = [kmeans.cluster_centers_[k][5] for k in range(len(kmeans.cluster_centers_))]

    plt.clf()
    plt.bar([1,2,3,4,5,6],metMinutes)
    plt.ylabel('metMinutes')
    plt.xlabel('Clusters')
    plt.savefig('metMinutes.pdf')  
    plt.clf()

    plt.bar([1,2,3,4,5,6],timeStart)
    plt.ylabel('timeStart')
    plt.xlabel('Clusters')
    plt.savefig('timeStart.pdf') 
    plt.clf()

    plt.bar([1,2,3,4,5,6],duration)
    plt.ylabel('duration')
    plt.xlabel('Clusters')
    plt.savefig('duration.pdf') 
    plt.clf()

    plt.bar([1,2,3,4,5,6],age)
    plt.ylabel('age')
    plt.xlabel('Clusters')
    plt.savefig('age.pdf') 
    plt.clf()

    plt.bar([1,2,3,4,5,6],gender)
    plt.ylabel('gender')
    plt.xlabel('Clusters')
    plt.savefig('gender.pdf') 
    plt.clf()

    plt.bar([1,2,3,4,5,6],clusterIntensities)
    plt.ylabel('Intensity')
    plt.xlabel('Clusters')
    plt.savefig('clusterIntensities.pdf') 
    plt.clf()
    
    
    
    



###How To Use###
#Run init() first. Afterwards get user belongig list back by providing getUserBelonging with key. See below:
#init()
#print(getUserBelonging("612C092CD05AD9F2F9E7A2D03526FDA5"))
#print(getUserBelonging("D0E1963A7D0C8AC343AE79A39D8F5CBE"))