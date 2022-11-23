import os
from pymongo import MongoClient
import re
import time

def listVenues(collection, num):
    print("Listing top " + str(num) + " venues...")

    start = time.time()

    # build a hashmap where key : article, value : every other article that references key
    referenced_by = {}

    # build another hashmap where key : venue, value : all articles of that venue
    venue_to_articles = {}

    for article in collection.find():

        aid = article['id']

        if 'venue' in article:
            vid = article['venue']
        else:
            vid = ""

        # store this id in the dictionary if not existing
        if aid not in referenced_by:
            referenced_by[aid] = []

        # then check all of this articles references
        if 'references' in article:
            references = article['references']
        else:
            continue

        # populate our references dictionary
        for reference in references:
            # make it so that the referenced article knows our current article references it
            if reference in referenced_by:
                referenced_by[reference].append(aid)
            else:
                referenced_by[reference] = [aid]

        # populate our venue dictionary
        if vid in venue_to_articles:
            venue_to_articles[vid].append(aid)
        else:
            venue_to_articles[vid] = [aid]

    # basic grouping by venue, gets article count
    venue_article_count = collection.aggregate([{'$match': {'venue': {'$not': re.compile('^(?![\s\S])')}}}, {'$group':{'_id' : '$venue', 'article_count' : {'$sum' : 1}}}])
    venue_article_count = list(venue_article_count)

    venue_copy = venue_article_count

    # maintain a list of the same size as venue
    # this list will have the number of total references per venue, to be used for sorting
    total_references = [0] * len(venue_copy)
    # print("length of list: " + str(len(venue_copy)))
    # for each distinct venue
    for i, venue in enumerate(venue_article_count):
        if venue['_id'] == '':
            continue

        # print whole thing for debugging
        # print(venue)

        # get the other info of that venue
        venue_name = venue['_id']
        articles = venue_to_articles[venue_name]
        # venue_info_cursor = collection.find({"venue": venue_name})

        # articles = [] # array that will store all articles from this venue
        ref_articles = set() # unique set that tracks which articles reference this venue

        # debug printing
        # iterate over each item in the venue_info
        # basically iterate over each article in this venue
        # for venue_info in venue_info_cursor:
        #     articles.append(venue_info['id'])
        
        # print("venue and article ids: " + venue_info['venue'] + ' ' + str(articles))

        # for each article, count how many others reference it
        total_reference_count = 0 # total references to venue
        for article in articles:
            reference_count = 0 # total references to this particular article

            # print("iterating over article: " + article + " in venue " + venue_info['venue'])
            # get all references to this particular article
            references = referenced_by[article]

            for aid in references:

                # we can avoid double-counting here by perhaps having a set
                # and ensuring that the same article is not included twice

                # print(article + " is referenced by: " + aid)

                # only count distinct
                if aid not in ref_articles:
                    reference_count += 1
                    ref_articles.add(aid)

            # print("total references to this article: " + str(reference_count))
            total_reference_count += reference_count

        # print("total references to venue " + venue_info['venue'] + ": " + str(total_reference_count))
        # print("adding " + str(total_reference_count) + " to index " + str(i))
        # print("")
        total_references[i] = total_reference_count

        # if count == int(num):
        #    break
            
        #count += 1

    # print("Printing total reference count list")
    # print(total_references)

    # print("Printing copy...")
    # for venue in venue_copy:
    #     print(venue)
    #     print(venue['_id'])

    combined_list = zip(venue_copy, total_references)
    # print("printing combined list...")
    # for item in combined_list:
    #     print(item)

    # sort by references per venue
    sorted_combined_list = sorted(combined_list, key=lambda x:x[1], reverse=True)
    # print("printing sorted combined list...")

    count = 0 # only print out how many the user wants
    for sorted_item in sorted_combined_list:
        print("Venue: " + sorted_item[0]['_id'] + " | Article count: " + str(sorted_item[0]['article_count']) + " | Referenced count: " + str(sorted_item[1]))
        count += 1
        if count == int(num):
            break
    
    end = time.time()
    print(str(end - start))