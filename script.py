import numpy as np
import pandas as pd
import random

ran_matrix = abs(np.random.normal(0,1,(100, 5)))

for k, vec in enumerate(ran_matrix):
    ran_matrix[k] = vec/sum(vec)

dist = np.zeros((100, 99))

for k, vec in enumerate(ran_matrix):
    for i, vec2 in enumerate(np.delete(ran_matrix, k, axis=0)):
        dist[k][i] = np.dot(vec, vec2)

def suggestions(dist_people, dict):
    suggestion = []
    close_people = [dist_people[1] for i in dist_people[0] if i > 0.7]
    intermediate_people = [dist_people[1] for i in dist_people[0] if i>0.3 and i<0.7]
    distant_people = [dist_people[1] for i in dist_people[0] if i<0.3]

    Love = random.sample(close_people, 2)
    Neutral = random.sample(intermediate_people, 2)
    Hate = random.sample(distant_people, 1)

    suggested_people = [Love, Neutral, Hate]
    for like in suggested_people:
        for people in like:
            suggestion.append(dict.get(people))

    return Love, Neutral, Hate




