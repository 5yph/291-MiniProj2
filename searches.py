import os
from pymongo import MongoClient

def searchArticle(collection, input):
    temp1 = (input.lower()).split()
    temp2 = ['\"' + t + '\"' for t in temp1]
    search = ""
    for temp in temp2:
        search += temp
        if temp is not temp2[-1]:
            search+= ' '
    results = collection.find({"$text": {"$search": search}})
    for result in results:
        print(result)

