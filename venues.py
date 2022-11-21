import os
from pymongo import MongoClient

def listVenues(collection, num):
    print("Listing top " + str(num) + " venues...")

    # get a count for each venue occurrence
    venue_count = collection.aggregate([{'$group':{'_id' : '$venue', 'count' : {'$sum' : 1}}}, {'$sort' : { 'count': -1 }}])

    for venue in venue_count:
        print(venue)

    '''
    cursor = collection.find()

    results = list(cursor)
    count = 0
    for result in results:
        print("\nArticle #" + str(count+1))
        print("\tID: " + result["id"] + 
            "\n\tTitle: " + result["title"] + 
            "\n\tYear: " + result["year"] + 
            "\n\tVenue: " + result["venue"] + "\n")
        count += 1
    '''










