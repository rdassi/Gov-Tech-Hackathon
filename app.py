# Import libraries
import sys
import json
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import pickle
import os
import predict as p
from sklearn.ensemble import GradientBoostingRegressor
from decouple import config
import requests
import geocoder
import pymongo
import csv
import json 
from pymongo import MongoClient 
import pandas as pd
cluster=MongoClient(config('db_url'))
db=cluster["FertilizerData"]
collection=db["FertilizerQueryData"]
# Load the model
model_yield= p.loadModel('PickledFiles/modelgb.pkl')
model_rf=p.loadModel('PickledFiles/modelrf.pkl')
model_fert=p.loadModel('PickledFiles/modelfert.pkl')
app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
#to resolve CORS error
# CORS(app)


@app.route('/',methods=['POST','GET'])
def location():
    if(request.method=='POST'):
        g = geocoder.ip('me')
        print(g.latlng)
        lat=g.latlng[0]
        print(100)
        longg=g.latlng[1]
        url = 'http://apis.mapmyindia.com/advancedmaps/v1/'+config('license_key')+'/rev_geocode?lat='+str(lat)+'&lng='+str(longg)
        r = requests.get(url = url) 
        # extracting data in json format 
        data = r.json() 
        print(data)
        # print(data['results'][0]['district'])
        # print(data['results'][0]['state'])
        district=data['results'][0]['district'].split(' ')[0]
        print(district)
        state=data['results'][0]['state']
        print(state)
        area=float(request.form['area'])
        print(50)
        crop,fert=p.prediction_crop(model=model_rf,model2=model_fert,district=district)
        result= {"Fertilizer Name": fert}
        finds=collection.find_one(result)
        n=finds['Nitrogen']
        pf=finds['Phosphorous']
        k=finds['Potassium']
        cropnow=crop[0][0].upper()+crop[0][1:]
        # print(cropnow)
        predictiony = p.prediction_yield(model_yield,area=area,crop=cropnow,state=state,district=district.upper())
        
        # N,P,K,pH,soil_moisture=p.fert_pred(cropnow,model_fert)
        # p.optimise(cropnow)
        # Take the first value of prediction
        return render_template("index.html", prediction= predictiony,crop=cropnow,fertiliser=fert,N=n,P=pf,K=k)
    else:

        return render_template("index.html")



if __name__ == "__main__":
    #run the app, set debug=True during testing
    app.run(debug=False)


