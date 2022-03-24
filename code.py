from matplotlib.markers import MarkerStyle
import numpy as np
import pandas as pd
import sklearn as sk
import matplotlib.pyplot as plt
import seaborn as sns
import umap

pandaRead = pd.read_json("./movedata.json")
reducer = umap.UMAP()


def timeToInt(time):
    hours = (time.split(":")[0])[:-1]
    minutes = time.split(":")[1]
    timeInt = int(minutes) + 60*int(hours)
    return timeInt


pandaRead["timeStart"] = pandaRead["timeStart"].map(lambda x: timeToInt(str(x)[-5:]))


tracker_data = pandaRead[
    [

        "metMinutes",
        "timeStart",
        "duration",
    ]
].values

embedding = reducer.fit_transform(tracker_data)
embedding.shape

plt.scatter(
    embedding[:, 0],
    embedding[:, 1],
    c=[sns.color_palette()[x] for x in [1]], s= [1])
plt.gca().set_aspect('equal', 'datalim')
plt.savefig('line_plot.pdf')  