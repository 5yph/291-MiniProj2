import subprocess
import os
import time
from pymongo import MongoClient, ASCENDING, TEXT


def main():
    print("-------------")
    print("BUILDING A DOCUMENT STORE")
    print("-------------")
    while(1):
        thisInput = input("Enter a json file name, and the port number under which the MongoDB server is running: ")

        splitInput = thisInput.split()
        if len(splitInput) is not 2:
            print("Incorrect number of arguments.")
            continue

        jsonFile = splitInput[0]

        port = int(splitInput[1])

        print("Connecting to MongoDB server at port:" , port, " ...")
        start = time.time()
        try:
            client = MongoClient('mongodb://localhost:{}'.format(port))
        except: 
            print("Failed to connect to MongoDB server. Try again.")
            continue

        print("Connected!")

        print("Creating database '291db' ...")

        try:
            db = client["291db"]
        except:
            print("Failed to create database. Try again.")
            continue

        print("Created database!")

        try:
            # List collection names.
            collist = db.list_collection_names()
        except:
            print("Timeout Error: Failed to open and load database. Check if the port number is available, and running the MongoDB Server.")
            continue



        if "dblp" in collist:
            print("Collection 'dblp' exists in the databse. Dropping the collection ...")
            db["dblp"].drop()
            print("Collection dropped.")

        # Create or open the collection in the db
        print("Creating collection 'dblp' ...")
        article_collection = db["dblp"]
        print("Collection created!")
        
        print("Importing contents of ", jsonFile, " to the collection ...")
        # pr = subprocess.Popen(['mongoimport', '--db', '291db', '--collection', 'dblp', '--file', jsonFile, '--jsonArray'])
        os.system("mongoimport --db 291db --port {} --collection dblp --file {}".format(port,jsonFile))
        print("Imported successfuly!")

        print("Dropping old indexs ...")
        article_collection.drop_indexes()

        print("Setting all years in entries to string ...")
        # set year to string for the text index
        article_collection.update_many({}, [{"$set": {"year": {"$toString": "$year"}}}])

        print("Creating indices on title, authors, abstract, venue and year ...")
        article_collection.create_index([
            ("title", TEXT),
            ("authors", TEXT),
            ("abstract", TEXT),
            ("venue", TEXT),
            ("year", TEXT),
            ("references", TEXT)
        ], default_language = "none")
        print("Created indices !")

        end = time.time()

        print(end - start)

        break

if __name__ == "__main__":
    main()