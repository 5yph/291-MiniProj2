import os
from pymongo import MongoClient

def searchArticle(collection, keywords):
    temp1 = (keywords.lower()).split()
    temp2 = ['\"' + t + '\"' for t in temp1]
    search = ""
    for temp in temp2:
        search += temp
        if temp is not temp2[-1]:
            search+= ' '
    cursor = collection.find({"$text": {"$search": search}})
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








