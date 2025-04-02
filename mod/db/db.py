from pymongo import MongoClient

db =MongoClient('mongodb+srv://sagaraliyas005:iDRnmctBwc0H3Q2x@cluster0.vo8fivl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')['RoadAssist']

user =db.user

seller = db.seller
order = db.order




