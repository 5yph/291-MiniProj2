import os
from pymongo import MongoClient

def listVenues(collection, num):
    print("Listing top " + str(num) + " venues...")

    # get a count for each article occurence per venue
    venue_count = collection.aggregate([{'$group':{'_id' : '$venue', 'article_count' : {'$sum' : 1}}}, {'$sort' : { 'article_count': -1 }}])

    # find a way to get number of articles that reference paper per venue

    # display venues in proper order
    count = 0
    for venue in venue_count:
        # exclude empty venue
        if venue['_id'] == '':
            continue

        # only print top n or less if doesn't exist
        if count == int(num):
            break
            
        print(venue)
        count += 1

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










