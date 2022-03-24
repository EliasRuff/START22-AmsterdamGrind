import sklearn.cluster as sk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


userBelongings = {}

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

def init(pandaActivity, pandaMove):
    global userBelongings
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

    userBelongings = {}

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

def getUserBelonging(key):
    global userBelongings
    return userBelongings[key]

###How To Use###
#Run init() first. Afterwards get user belongig list back by providing getUserBelonging with key. See below:
#init()
#print(getUserBelonging("612C092CD05AD9F2F9E7A2D03526FDA5"))
#print(getUserBelonging("D0E1963A7D0C8AC343AE79A39D8F5CBE"))