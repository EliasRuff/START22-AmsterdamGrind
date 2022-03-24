from torch import normal
from belonging import *
#from get_user_activity import *
from sklearn.preprocessing import normalize
from script import suggestions

uid = 'D0E1963A7D0C8AC343AE79A39D8F5CBE'
activities = pd.read_json('./activities.json')
pandaMove = pd.read_json("./movedata.json")
users = pd.read_json("./users.json")

belongingsDict = init(activities,pandaMove)
def getSimilarUsers(key):
    maxVal = 0
    distanceToUsers = []
    clusterAffiliation = belongingsDict[key]
    
    
    for vals in users.values:
        id = vals[0]
        dist = np.linalg.norm(np.subtract(clusterAffiliation, belongingsDict[id]))
        distanceToUsers.append([dist, id])
        maxVal = max(maxVal, dist)
    return suggestions(distanceToUsers, maxVal)




print(getSimilarUsers(uid))
  
#print(getUserBelonging(uid))
#print(get_user_activity(activities, uid))
