from pymongo import MongoClient
from insert import insertArticle
from searches import searchArticle, searchAuthors
from venues import listVenues




def uMenu(collection):
    # client = MongoClient('mongodb://localhost:{}'.format(20202))
    # db = client["291db"]
    # collection = db["dblp"]
    print("")
    print("User Menu")
    print("---------")

    print("You've created a MongoloidDB database! What would you like to do now?")
    sno = None
    while (1):
        print("Select an option: ")
        print("1: Search for Articles")
        print("2: Search for Authors")
        print("3: List the Venues")
        print("4: Add an Article")
        print("q: Quit")
        x = input()
        if (x not in ['1','2','3','4','q']):
            print("Please put a valid input !")
            continue
        elif (x == '1'):
            y = input("Enter some space separated inputs yo !\n")
            if (y == ""):
                print("Bad input !")
                continue 
            searchArticle(collection, y)
            continue
        elif (x == '2'):
            y = input("Enter some space separated inputs yo !\n")
            if (y == ""):
                print("Bad input !")
                continue 
            searchAuthors(collection, y)    
            continue
        elif (x == '3'):
            n = input("Enter how many top venues you'd like to see!\n")
            listVenues(collection, n)
            continue

        elif (x == '4'):

            while(1):
                thisID = input("Enter a unique ID: ")
                if thisID == "" or thisID.isspace():
                    print("Please give a unique ID.")
                    continue
                cursor = collection.find({"id": thisID})
                results = list(cursor)
                con = 0
                for result in results:
                    con += 1
                if con > 0:
                    print("ID exists. Give unique ID.")
                    continue
                else:
                    break

            while (1):
                title = input("Enter a title: ")
                if title == "" or title.isspace():
                    print("Please give a title.")
                    continue
                else:
                    break

            while (1):
                authors = input("Give a list of authors (space seperated): ")
                if authors == "" or authors.isspace():
                    print("Please give a list of authors.")
                    continue
                else:
                    authors = authors.split()
                    break

            while (1):
                year = input("Give a year: ")
                if year == "" or year.isspace():
                    print("Please give a year.")
                    continue
                elif year.isdigit() == False:
                    print("Year given is not a proper number.")
                    continue
                else:
                    break

            insertArticle(collection, authors, title, year, thisID)

            continue

        elif (x == 'q'):
            print('Thank you for using MongoloidDB Data Storing Program!')
            print("Exiting ...")
            break

# if __name__ == "__main__":
#     main()

# Add an article The user should be able to add an article to the collection by providing a unique id, a title, a list of authors, and a year. The fields abstract and venue should be set to null, references should 
# be set to an empty array and n_citations should be set to zero. 