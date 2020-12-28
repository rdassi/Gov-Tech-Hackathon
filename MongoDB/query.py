import pymongo
import csv
import json 
from decouple import config
from pymongo import MongoClient 
import pandas as pd
cluster=MongoClient(config('db_url'))
db=cluster["FertilizerData"]
collection=db["FertilizerQueryData"]

result= {"Fertilizer Name": "20-20"}
finds=collection.find_one(result)
n= finds['Nitrogen']
p=finds['Phosphorous']
k=finds['Potassium']
