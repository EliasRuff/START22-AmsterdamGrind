import os
from queue import Empty
from re import M
import sys
from main import *
import datetime

testuser = 'D0E1963A7D0C8AC343AE79A39D8F5CBE'

userdata = get_user_activity(activities, testuser)

similarUsers = getSimilarUsers(testuser) # List of list of GUIDs

def isDateFarInPast(toTest, reference):
    toTestDate = datetime.datetime(int(toTest[:4]), int(toTest[5:7]), int(toTest[8:10]), tzinfo=datetime.timezone.utc)
    referenceDate = datetime.datetime(int(reference[:4]), int(reference[5:7]), int(reference[8:10]), tzinfo=datetime.timezone.utc)
    return (toTestDate.timestamp() + 16070400) < referenceDate.timestamp()

def hatesSuggestion(data):
    if data.empty:
        return True
    bestGuess = data.iloc[0]
    matchingRow = None
    for index, row in userdata.iterrows():
        if row['category_type'] == bestGuess['category_type'] and row['subcat'] == bestGuess['subcat']:
            matchingRow = row
            break
    if not isinstance(matchingRow, pd.DataFrame):
        return False
    else:
        if isDateFarInPast(bestGuess['activityTime'], matchingRow['activityTime']):
            return matchingRow['percentage'].any() < 0.25
        else:
            return False

def coach_activity(coach_catalogue,category,subcategory,n):
    possible_suggestions = coach_catalogue[coach_catalogue.category.str.contains(category) & coach_catalogue.subcategory.str.contains(subcategory)]
    try:
        return possible_suggestions.sample(n)
    except:
        return None

def printSuggestion(guidList, suggesstionComment):
    for guid in guidList:
        guid = get_user_activity(activities, guid)
        if hatesSuggestion(guid):
                continue
        else:
            detailedSuggestions = coach_activity(coach_catalogue, guid.iloc[0]['category_type'], guid.iloc[0]['subcat'],1)
            print(suggesstionComment + detailedSuggestions.iloc[0]['name'])

while(True):
    while(True):
        val = input("Are you ready for a suggestion? (y): ")
        if val == 'y':
            break

    printSuggestion(similarUsers[0], "You might enjoy: ")
    printSuggestion(similarUsers[1], "Others enjoyed: ")
    printSuggestion(similarUsers[2], "Have you heard of: ")