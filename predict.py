#importing
import numpy as np
import pickle
import pandas as pd
import math
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
import pickle



# predicting yield from crop, season, mapmyindia api data and user input
def prediction_yield(model,data,area=1254, district='NICOBARS',crop='Arecanut', season='Kharif     ', state='Andaman and Nicobar Islands'):
    print(crop)
    # data=pd.read_csv('data/indiaselected.csv')
    

    #creating categorical labels or codes for all the values and storing it as a separate dataframe
    data1=pd.DataFrame()
    data1['State_Name']=data['State_Name'].astype('category').cat.codes
    data1['District_Name']=data['District_Name'].astype('category').cat.codes
    data1['Season']=data['Season'].astype('category').cat.codes
    data1['Crop']=data['Crop'].astype('category').cat.codes
    data1['Area']=data['Area']
    data1['Production']=data['Production']

    # creating a dictionary of category codes and the value
    d_state = dict(enumerate(data['State_Name'].astype('category').cat.categories))
    d_district = dict(enumerate(data['District_Name'].astype('category').cat.categories))
    d_season = dict(enumerate(data['Season'].astype('category').cat.categories))
    d_crop = dict(enumerate(data['Crop'].astype('category').cat.categories))
    
    # print(d_season)

    #finding the corresponding codes for user input
    for x in d_state:

        y=d_state[x]
        if(y==state):
            statecode=x

    for x in d_district:
        y=d_district[x]
        if(y==district):
            districtcode=x

    for x in d_season:
        y=d_season[x]
        if(y==season):
            seasoncode=x
    
    for x in d_crop:
        y=d_crop[x]
        if(y==crop):
            cropcode=x
            

    
    
    #loading the scaler fit on training data
    scaler=pickle.load(open('PickledFiles/scalergb.sav','rb'))

    #creating a vector of the input features
    x=np.array([statecode,districtcode,seasoncode,cropcode,area])

    #scaling input features
    newx=scaler.transform(x.reshape(1,-1))

    #returning prediction
    return math.exp(model.predict(newx))

#crop prediction and fertiliser prediction from weather api data
def prediction_crop(model,model2,temperature=25.567483, humidity=60.492446, rainfall=190.225784,district='Bangalore'):
    print(district)
    
    #sending get request to the weather api
    response = requests.get("http://api.weatherapi.com/v1/forecast.json?key=6e1498be712f43a081f200018203110&q="+district+"&days=10",)
    # print(response.status_code)

    #converting the request object to json
    x=response.json()

    #converting the json to dataframe and picking the relevant fields for forecast
    y=pd.DataFrame.from_records(x)
    z=y['forecastday':'name']
    f=z['forecast']['forecastday']


    #taking the average for three day forecasts
    sum=0
    for i in range(3):
      sum=sum + f[i]['day']['avgtemp_c']
    temperature=sum/3

    sum=0
    for i in range(3):
      sum=sum + f[i]['day']['totalprecip_mm']
    rainfall=(sum/3)*100

    sum=0
    for i in range(3):
      sum=sum + f[i]['day']['avghumidity']
    humidity=sum/3


    #creating feature vector out of the forecasted averages
    x=np.array([temperature, humidity, rainfall+5]) #adding a small smoothing parameter for 0 rainfall
    print(x)

    #loading the scaler fit on the training data
    scalerrf=pickle.load(open('PickledFiles/scalerrf.sav','rb'))

    #scale the input features
    newx=scalerrf.transform(x.reshape(1,-1))

    #creating a feature vector of temp and himidity for the fertiliser model
    x2=np.array([temperature, humidity])

    #loading the dictionary that maps fertliser labels to fertiliser names
    d=pickle.load(open('PickledFiles/dict.pkl','rb'))

    #return crop prediction and fertiliser prediction
    return model.predict(newx), d[model2.predict(x2.reshape(1,-1))[0]]


# function to load pickled ML models
def loadModel(filename):
    with open(filename, 'rb') as f:
            model = pickle.load(f)
    return model
    




    
    



    
    