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
from pymongo import MongoClient 
import pandas as pd
import time

#getting the cluster from the database url
cluster=MongoClient(config('db_url'))

#accessing the fertliser data
db=cluster["FertilizerData"]

#getting the subset that corresponds to querying 
collection=db["FertilizerQueryData"]

# Load the models
model_yield= p.loadModel('PickledFiles/modelgb.pkl')
model_rf=p.loadModel('PickledFiles/modelrf.pkl')
model_fert=p.loadModel('PickledFiles/modelfert.pkl')

#app instance
app = Flask(__name__, static_url_path='/static')

#allows cross origin requests for location
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# for the / route, render index.html template under two conditions
@app.route('/',methods=['POST','GET'])
def location():

    #if the submit button has been clicked
    if(request.method=='POST'):

        #get the latitude and logitude corresponding to the user's IP address
        g = geocoder.ip('me')
        print(g.latlng)

        lat=g.latlng[0]
        longg=g.latlng[1]

        #send the latitiude and longitude to the mapmyindia api to get the district, state names
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

        #getting area from the form 
        area=float(request.form['area'])
    
        #predicting the crop using the district as input to weather api, which further gives weather input features to model,
        #and also using weather data to predict fertiliser
        crop,fert=p.prediction_crop(model=model_rf,model2=model_fert,district=district)

        #use the predicted fertiliser to query npk values
        result= {"Fertilizer Name": fert}
        finds=collection.find_one(result)
        n=finds['Nitrogen']
        pf=finds['Phosphorous']
        k=finds['Potassium']

        #convert the crop to proper case for the yield prediction model
        cropnow=crop[0][0].upper()+crop[0][1:]
        # print(cropnow)

        #get current month
        month=time.strftime("%m") 
        print(month)

        #dictionary that maps seasons to months
        seasons={'Kharif     ': ['7', '8', '9', '10'],
                'Autumn     ': ['9', '10', '11'],
                'Summer     ': ['3', '4', '5', '6'],
                'Winter     ': ['12','1','2'],
                'Rabi       ': ['10','11','12','1','2','3'],
                'Whole Year ': ['1','2','3', '4', '5', '6','7', '8', '9', '10','11','12']}

        #pick all seasons for the current month
        s=[]
        for key,value in seasons.items():
            # print(value)
            for val in value:
                if(val==month):
                    s.append(key)
                    break
        print(s)
        #store the yield prediction for each season in a list
        predictions=[]
        for season in s:
            print(season)
            predictions.append(p.prediction_yield(model_yield,area=area,season=season,crop=cropnow,state=state,district=district.upper()))
        
        print(predictions)
        
        #render template with predicted values (average yield, crop, NPK values, fertliser name)
        return render_template("index.html", prediction= sum(predictions)/len(predictions),crop=cropnow,fertiliser=fert,N=n,P=pf,K=k)
    
    #loading the website before user has entered values
    else:

        #render template with blank table
        return render_template("index.html")



if __name__ == "__main__":
    #run the app, set debug=True during testing
    app.run(debug=False)


