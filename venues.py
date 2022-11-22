import os
from pymongo import MongoClient
import re

def listVenues(collection, num):
    print("Listing top " + str(num) + " venues...")

    # basic grouping by venue, gets article count
    venue_article_count = collection.aggregate([{'$match': {'venue': {'$not': re.compile('^(?![\s\S])')}}}, {'$group':{'_id' : '$venue', 'article_count' : {'$sum' : 1}}}, {'$sort' : { 'article_count': -1 }}])
    venue_article_count = list(venue_article_count)
    

    venue_copy = venue_article_count
    # venue_copy.remove('')

    # get the references per each venue
    # count = 0 

    # maintain a list of the same size as venue
    # this list will have the number of total references per venue, to be used for sorting
    total_references = [0] * len(venue_copy)
    print("length of list: " + str(len(venue_copy)))
    # for each distinct venue
    for i, venue in enumerate(venue_article_count):
        if venue['_id'] == '':
            continue

        # print whole thing for debugging
        print(venue)

        # get the other info of that venue
        venue_name = venue['_id']
        venue_info_cursor = collection.find({"venue": venue_name})

        articles = [] # array that will store all articles from this venue

        # debug printing
        # iterate over each item in the venue_info
        # basically iterate over each article in this venue
        for venue_info in venue_info_cursor:
            articles.append(venue_info['id'])
        
        print("venue and article ids: " + venue_info['venue'] + ' ' + str(articles))

        # for each article, count how many others reference it
        total_reference_count = 0 # total references to venue
        for article in articles:
            reference_count = 0 # total references to this particular article

            print("iterating over article: " + article + " in venue " + venue_info['venue'])
            reference_to_this_article_cursor = collection.find({"references": article})

            for reference_info in reference_to_this_article_cursor:

                # we can avoid double-counting here by perhaps having a set
                # and ensuring that the same article is not included twice?

                print(article + " is referenced by: " + str(reference_info['id']))
                reference_count += 1
            print("total references to this article: " + str(reference_count))
            total_reference_count += reference_count

        print("total references to venue " + venue_info['venue'] + ": " + str(total_reference_count))
        print("adding " + str(total_reference_count) + " to index " + str(i))
        print("")
        total_references[i] = total_reference_count

        # if count == int(num):
        #    break
            
        #count += 1

    print("Printing total reference count list")
    print(total_references)

    print("Printing copy...")
    for venue in venue_copy:
        print(venue)
        print(venue['_id'])

    combined_list = zip(venue_copy, total_references)
    # print("printing combined list...")
    # for item in combined_list:
    #     print(item)

    # sort by references per venue
    sorted_combined_list = sorted(combined_list, key=lambda x:x[1], reverse=True)
    print("printing sorted combined list...")
    for sorted_item in sorted_combined_list:
        print(sorted_item)
    
