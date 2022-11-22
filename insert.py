import os
from pymongo import MongoClient

def insertArticle(collection, authors, title, year, thisID):
    print("Inserting entry into collection ...")
    article = { "abstract": None, "authors": authors, "n_citations": 0, "references": [], "title": title, "venue": None, "year": year, "id": thisID}
    collection.insert_one(article)
    print("Finished inserting!")