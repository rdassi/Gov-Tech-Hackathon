import pymongo
import csv
import json 

from pymongo import MongoClient 
import pandas as pd
cluster=MongoClient("mongodb+srv://neelb:Fertilizer123@fertilizer.244tu.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=cluster["FertilizerData"]
collection=db["FertilizerQueryData"]

result= {"Fertilizer Name": "20-20"}
finds=collection.find_one(result)
n= finds['Nitrogen']
p=finds['Phosphorous']
k=finds['Potassium']
