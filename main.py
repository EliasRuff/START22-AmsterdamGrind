from belonging import *
from get_user_activity import *

uid = 'D0E1963A7D0C8AC343AE79A39D8F5CBE'
activities = pd.read_json('./activities.json')
pandaMove = pd.read_json("./movedata.json")

init(activities,pandaMove)
print(getUserBelonging("D0E1963A7D0C8AC343AE79A39D8F5CBE"))
print(get_user_activity(activities, uid))