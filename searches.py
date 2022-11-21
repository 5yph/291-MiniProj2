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
        print("\tID: " + result["id"] + 
            "\n\tTitle: " + result["title"] + 
            "\n\tYear: " + result["year"] + 
            "\n\tVenue: " + result["venue"] + "\n")
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
                print("\tID: " + results[int(y)-1]["id"] + 
                    "\n\tTitle: " + results[int(y)-1]["title"] + 
                    "\n\tYear: " + results[int(y)-1]["year"] + 
                    "\n\tVenue: " + results[int(y)-1]["venue"])
                if ("abstract" in results[int(y)-1]): 
                    print("\tAbstract: " + results[int(y)-1]["abstract"])
                authnum = 1
                for author in results[int(y)-1]["authors"]:
                    print("\tAuthor #" + str(authnum) + ": " + author)
                    authnum += 1
                subcursor = collection.find({"references": results[int(y)-1]["id"]})
                refnum = 1
                for reference in subcursor:
                    print("References to Article " + y + ":")
                    print("Reference #: " + str(refnum))
                    print("\tID: " + reference["id"] + 
                        "\n\tTitle: " + reference["title"] + 
                        "\n\tYear: " + reference["year"])
                    refnum += 1








