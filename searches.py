import os
#import time
from pymongo import MongoClient

def searchArticle(collection, keywords):
    temp1 = (keywords.lower()).split()
    temp2 = ['\"' + t + '\"' for t in temp1]
    search = ""
    for temp in temp2:
        search += temp
        if temp is not temp2[-1]:
            search+= ' '
    
    #start = time.time()
    #original cursor
    cursor = collection.find({"$text": {"$search": search}})
    #modified cursor with aggregate (who tf knows if this makes it better)
    #cursor = collection.aggregate([{"$match": {"$text": {"$search": search}}}])
    #end = time.time()
    #print(end - start)

    results = list(cursor)
    count = 0
    for result in results:
        print("\nArticle #" + str(count+1))
        if (result["id"] is not None): print("\tID: " + result["id"])
        if (result["title"] is not None): print("\tTitle: " + result["title"])
        if (result["year"] is not None):print("\tYear: " + result["year"])
        if (result["venue"] is not None): 
            print("\tVenue: " + result["venue"] + "\n")
        else:
            print("\tVenue: NA")
        count += 1
    if results:
        while (1):
            x = input("Would you like to see the full details of an article ? ! ? (Y/N): ")
            if (x.lower() == 'n'):
                print("Oh well !")
                break
            elif (x.lower() == 'y'):
                y = input("Choose the article number from the list above (Not ID) !: ")
                if (int(y) < 1 or int(y) > len(results)):
                    print("Bad article number!")
                    continue
                else:
                    print("\nArticle #" + y + ":")
                    if (results[int(y)-1]["id"] is not None): print("\tID: " + results[int(y)-1]["id"]) 
                    if (results[int(y)-1]["title"] is not None): print("\tTitle: " + results[int(y)-1]["title"]) 
                    if (results[int(y)-1]["year"] is not None): print("\tYear: " + results[int(y)-1]["year"]) 
                    if (results[int(y)-1]["venue"] is not None): print("\tVenue: " + results[int(y)-1]["venue"])
                    if ("abstract" in results[int(y)-1]): 
                        if (results[int(y)-1]["abstract"] is not None): 
                            print("\tAbstract: " + results[int(y)-1]["abstract"])
                        else:
                            print("\tAbstract: NA")
                    authnum = 1
                    for author in results[int(y)-1]["authors"]:
                        print("\tAuthor #" + str(authnum) + ": " + author)
                        authnum += 1
                    subcursor = collection.find({"references": results[int(y)-1]["id"]})
                    refnum = 1
                    for reference in subcursor:
                        print("References to Article " + y + ":")
                        print("Reference #: " + str(refnum))
                        if (reference["id"] is not None): print("\tID: " + reference["id"])
                        if (reference["title"] is not None): print("\tTitle: " + reference["title"])
                        if (reference["year"] is not None): print("\tYear: " + reference["year"])
                        refnum += 1

def searchAuthors(collection, keyword):
    search = '\"' + keyword + '\"'
    cursor = collection.find({"$text": {"$search": search}})
    results = cursor
    authors = []
    for result in results:
        resauthors = result["authors"]
        for resauthor in resauthors:
            temp = (resauthor.lower()).split()
            if keyword.lower() in temp and resauthors not in authors:
                authors.append(resauthors)
    regex = ".*" + keyword + ".*"
    subcursor = collection.aggregate([
        {"$match": {"authors": {"$in": authors}}},
        {"$project": { "_id": 0, "authors": 1 } },
        {"$unwind": "$authors" },
        {"$group" : {"_id": {"authors" : "$authors"}, "articles" : {"$sum" : 1} }},
        {"$match": {"_id.authors": {"$regex": regex, "$options": "i"}}}
    ])
    print()
    matches = list(subcursor)
    authcount = 1
    for match in matches:
        print("Author #" + str(authcount) + ": " + match["_id"]["authors"] + " | Article Count: " + str(match["articles"]))
        authcount += 1
    if authors:
        while (1):
            x = input("Would you like to see the full details of an author ? ! ? (Y/N): ")
            if (x.lower() == 'n'):
                print("Oh well !")
                break
            elif (x.lower() == 'y'):
                y = input("Type the author's full name with correct punctuation from the list (Not ID) !: ")
                print("")
                if (y == ""):
                    print("Bad author name!")
                    continue
                else:
                    subcursor = collection.aggregate([
                        {"$match": {"authors": y}},
                        {"$project": { "_id": 0, "authors": 1, "title": 1, "year": 1, "venue": 1 }},
                        {"$sort": {"year": -1}}
                    ])
                    returns = subcursor
                    print(y + "'s Articles:")
                    for ret in returns:
                        if (ret["venue"] is not None):
                            print("\t" + ret["title"] + ', ' + ret["year"] + ' in ' + ret["venue"])
                        else:
                            print("\t" + ret["title"] + ', ' + ret["year"])
                    print("")
