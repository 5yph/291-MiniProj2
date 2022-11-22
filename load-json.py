import subprocess
import os
from pymongo import MongoClient, ASCENDING, TEXT
import time


def main():
    print("-------------")
    print("MONGOLOIDDB DATA STORING PROGRAM")
    print("-------------")
    thisInput = input("Enter a json file name, and the port number under which the MongoDB server is running: ")


    splitInput = thisInput.split()

    jsonFile = splitInput[0]

    port = int(splitInput[1])

    print("Connecting to MongoDB Server at port:" , port, " ...")
    client = MongoClient('mongodb://localhost:{}'.format(port))
    print("Connected!")

    print("Creating database '291db' ...")
    db = client["291db"]
    print("Created database!")

    # List collection names.
    collist = db.list_collection_names()

    if "dblp" in collist:
        print("Collection 'dblp' exists in the databse. Dropping the collection ...")
        db["dblp"].drop()
        print("Collection dropped.")

    # Create or open the collection in the db
    print("Creating collection 'dblp' ...")
    article_collection = db["dblp"]
    print("Collection created!")

    start = time.time()
    print("Importing contents of ", jsonFile, " to the collection ...")
    # pr = subprocess.Popen(['mongoimport', '--db', '291db', '--collection', 'dblp', '--file', jsonFile, '--jsonArray'])
    os.system("mongoimport --db 291db --port {} --collection dblp --file {}".format(port,jsonFile))
    print("Imported successfuly!")

    # set year to string for the text index
    article_collection.update_many({}, [{"$set": {"year": {"$toString": "$year"}}}])

    print("Creating indices on title, authors, abstract, venue and year !")
    article_collection.create_index([
        ("title", TEXT),
        ("authors", TEXT),
        ("abstract", TEXT),
        ("venue", TEXT),
        ("year", TEXT),
        ("references", TEXT)
    ])#, default_language = "english")
    print("Created indices !")
    end = time.time()
    print("Time taken: " + str(end - start))

    # results = article_collection.find({})
    # for rental in results:
    #     print(rental)


# For this part, you will write a program, named load-json with a proper extension (e.g. load-json.py if using Python), which will take a json file in the current directory and constructs a MongoDB collection. 
# Your program will take as input a json file name and a port number under which the MongoDB server is running, will connect to the server and will create a database named 291db (if it does not exist). Your program 
# then will create a collection named dblp. If the collection exists, your program should drop it and create a new collection. Your program for this phase ends after building the collection.

#Important Note: The input file is expected to be too large to fit in memory and you are expected to process it as one-row-at-a time, and not to fully load the file into memory. You may find Mongoimport helpful, 
# and you may change the default batch size (if needed) to allow loading large files on lab machines.

# """This is an example python script to work with the mongodb database using the
# pymongo library.

# We are going to model the ER diagram we had for the video-store
# application as part of mongo db.
# """

# from pymongo import MongoClient

# # Use client = MongoClient('mongodb://localhost:27017') for specific ports!
# # Connect to the default port on localhost for the mongodb server.
# client = MongoClient()


# # Create or open the video_store database on server.
# db = client["video_store"]


# # List collection names.
# collist = db.list_collection_names()
# if "movies_collection" in collist:
#     print("The collection exists.")

# # Create or open the collection in the db
# movies_collection = db["movies_collection"]

# # delete all previous entries in the movies_collection
# # specify no condition.
# movies_collection.delete_many({})

# # Insert movies into the collection. Remember that each inserted document should be key-value pairs.
# # movie num will be the provided _id when inserting into the collection.
# movies = [
#     {"title": "The matrix 4", "category_name": "action", "formats": ["VCD", "CD"]},
#     {"title": "Spiderman 6", "category_name": "sci-fi", "formats": ["CD", "Blueray"]},
#     {"title": "Spiderman 1", "category_name": "sci-fi", "formats": ["CD"]},
#     {"title": "La la Land", "category_name": None, "formats": ["DVD"]},
# ]

# # insert movies into the movies_collection.
# # use insert_one() to insert a single document.
# ret = movies_collection.insert_many(movies)

# # Print list of the _id values of the inserted documents
# movie_ids = ret.inserted_ids
# print(movie_ids)


# members = [
#     {
#         "_id": "7806808181",
#         "name": "Saeed",
#         "like": "action",
#         "dependents": ["Saeed Junior", "Saeed J Junior"],
#         "member_type": "Gold",
#         "credit number": "450 80 81",
#     },
#     {
#         "_id": "6806808282",
#         "name": "Mike",
#         "like": "drama",
#         "dependents": None,
#         "member_type": "Bronze",
#         "credit number": None,
#     },
# ]

# # Insert members into a new collection.
# members_collection = db["members_collection"]

# # delete previous docs in the members collection.
# members_collection.delete_many({})

# ret = members_collection.insert_many(members)
# member_ids = [mem["_id"] for mem in members]


# rental_collection = db["rentals_collection"]

# """ Rules:
# You cannot rent a movie if it has already rented out.
# Gold members are free to rent any number of movies they want.
# Bronze and dependents can only rent one movie.
# """

# rental = {"member_renting": ("Saeed", "7806808181"), "movie_rented": movie_ids[0]}
# # delete previous docs in the rental_collection
# rental_collection.delete_many({})
# rental_collection.insert_one(rental)


# def get_the_member(db, member_name, member_phone_number):
#     """Check the documents in the members collection to specify the type of the
#     member."""
#     mem_coll = db["members_collection"]
#     results = mem_coll.find({"_id": member_phone_number})
#     for mem in results:
#         if mem["name"] == member_name:
#             return mem["member_type"]
#         if mem["dependents"] is not None and member_name in mem["dependents"]:
#             return "Dependent"


# def check_movie_for_member(db, member_name, member_phone_number, movie_id):
#     """Function to query the database for some of the checks."""

#     # check if movie_id has been rented out or not.
#     rent_coll = db["rentals_collection"]
#     results = rent_coll.find({"movie_rented": movie_id})
#     results_count = rent_coll.count_documents({"movie_rented": movie_id})
    
#     if results_count > 0:
#         print("This movie {0} has been rented out".format(movie_id))
#         return False

#     results = rent_coll.find({"member_renting": (member_name, member_phone_number)})
    
#     # count the number of movies this person is watching currently.
#     num_movies = rent_coll.count_documents({"member_renting": (member_name, member_phone_number)})
    
#     member_type = get_the_member(db, member_name, member_phone_number)
    
#     if member_type == "Dependent" and num_movies > 0:
#         print("Dependent can only rent one movie")
#         return False
#     if member_type == "Bronze" and num_movies > 0:
#         print("Bronze member can only rent one movie")
#         return False

#     return True


# # This won't work since the movie is rented out.
# if check_movie_for_member(db, "Saeed Junior", "7806808181", movie_ids[0]):
#     rental_collection.insert_one(
#         {"member_renting": ("Saeed Junior", "7806808181"), "movie_rented": movie_ids[0]}
#     )

# if check_movie_for_member(db, "Saeed Junior", "7806808181", movie_ids[1]):
#     rental_collection.insert_one(
#         {"member_renting": ("Saeed Junior", "7806808181"), "movie_rented": movie_ids[1]}
#     )

# if check_movie_for_member(db, "Mike", "6806808282", movie_ids[2]):
#     rental_collection.insert_one(
#         {"member_renting": ("Mike", "6806808282"), "movie_rented": movie_ids[2]}
#     )

# # This won't work since the Mike is a bronze member.
# if check_movie_for_member(db, "Mike", "6806808282", movie_ids[3]):
#     rental_collection.insert_one(
#         {"member_renting": ("Mike", "6806808282"), "movie_rented": movie_ids[3]}
#     )


# # print all rentals
# results = rental_collection.find({}).sort("movie_rented")
# for rental in results:
#     print(rental)

# """ Expect to see these in the output:
# This movie 5f87720ba450f7bc9a730b03 has been rented out
# Bronze member can only rent one movie
# {'movie_rented': ObjectId('5f87720ba450f7bc9a730b02'), '_id': ObjectId('5f87720ba450f7bc9a730b07'), 'member_renting': ['Saeed Junior', '7806808181']}
# {'movie_rented': ObjectId('5f87720ba450f7bc9a730b03'), '_id': ObjectId('5f87720ba450f7bc9a730b06'), 'member_renting': ['Saeed', '7806808181']}
# {'movie_rented': ObjectId('5f87720ba450f7bc9a730b04'), '_id': ObjectId('5f87720ba450f7bc9a730b08'), 'member_renting': ['Mike', '6806808282']}
# """


if __name__ == "__main__":
    main()