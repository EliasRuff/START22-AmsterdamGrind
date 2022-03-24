import pandas as pd
import seaborn as sns
sns.set(font_scale=1.2, style="whitegrid", palette='magma')
import matplotlib.pyplot as plt
import json

move_data = pd.read_json('.//data//movedata.json')
activities = pd.read_json('.//data//activities.json')

def expand_activity_data(activity_data):
  def map_plain(x):
    try:
      json_obj = json.loads(x)
      return ''
    except Exception as e:
      return x
  def map_activity(x):
    try:
      json_obj = json.loads(x)['ActivityType']
    except Exception as e:
      return ''
    return json_obj
  def map_category_type(x):
    try:
      json_obj = json.loads(x)['CategoryType']
      if(json_obj == 'Movement activity completed'):
        return 'Movement'
      if(json_obj == 'Nutrition activity completed'):
        return 'Nutrition'
      if(json_obj == 'Mindfulness activity completed'):
        return 'Mindfulness'
      else:
        return json_obj
    except Exception as e:
      return ''
  def map_subcat(x):
    try:
      json_obj = json.loads(x)['SubcategoryType']
      if(json_obj == 'Flexibility excercise completed'):
        return 'Flexibility'
      if(json_obj == 'Strength excercise completed'):
        return 'Strength'
      if(json_obj == 'HealthyEating  completed'):
        return 'Healthy Eating'
      if(json_obj == 'Relaxation excercise completed'):
        return 'Relaxation'
      if(json_obj == 'Endurance excercise completed'):
        return 'Endurance'
      if(json_obj == 'Sleeping excercise completed'):
        return 'Sleep'
      if(json_obj == 'Weighttraining excercise completed'):
        return 'Strength'
      if(json_obj == 'Motivation excercise completed'):
        return 'Motivation'
      if(json_obj == 'Focus excercise completed'):
        return 'Concentration'
    except Exception as e:
      return ''
    return json_obj



  plain_col          = activity_data.activityDetails.apply(map_plain)
  activity_col       = activity_data.activityDetails.apply(map_activity)
  category_type_col  = activity_data.activityDetails.apply(map_category_type)
  subcat_col         = activity_data.activityDetails.apply(map_subcat)
  
  aggregate = {
    'id': activities.id,
    'plain': plain_col,
    'activity': activity_col,
    'category_type': category_type_col,
    'subcat': subcat_col,
  }
  jon_cols_data = pd.DataFrame(aggregate)
  return pd.merge(left=activities,right=jon_cols_data,on='id')


def get_user_activity(activity_data, userId):
  full_activity_data = expand_activity_data(activity_data)

  user_activity_data = full_activity_data[full_activity_data.userId==userId]
  activities = user_activity_data[['id','userId','category_type','subcat']].groupby(['userId','category_type','subcat']).count().reset_index()
  activities = activities.sort_values('id',ascending=False)
  activities = activities[activities.category_type!='']
  activity_count = activities.sum().id
  percentage = activities.id.divide(activity_count)
  activities['percentage'] = percentage
  return activities[['category_type', 'subcat', 'percentage']]


uid = 'AC98C327250EEA5DDE57783F6F21FF95'
print(get_user_activity(activities, uid))
