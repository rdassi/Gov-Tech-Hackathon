import pymongo
import csv
import json 
from decouple import config
from pymongo import MongoClient 
import pandas as pd
cluster=MongoClient(config("db_url"))
db=cluster["FertilizerData"]
collection=db["IndiaSelect"]
df= pd.read_csv('/Users/neelbhandari/Desktop/GovTech/FertilizerPrediction.csv',encoding="utf-8")

def csv_to_json(filename, header=None):
    data = pd.read_csv(filename, header=header)
    return data.to_dict('records')
collection.insert_many(csv_to_json('/Users/neelbhandari/Desktop/GovTech/indiaselected.csv', header=0))
# for i in range(rows):
#     post= {"temperature": df['Temparature'][i], "humidity":df['Humidity '][i], "moisture":df['Moisture'][i],"soil":df['Soil Type'][i],"crop_type":df['Nitrogen'][i],"potassium":df['Potassium'][i],"phosphrous":df['Phosphorous'][i],"fertilizer":df['Fertilizer Name'][i]}
#     collection.insert_one(post)