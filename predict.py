#importing
import numpy as np
import pickle
import pandas as pd
import math
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
import pickle

# function to load pickled ML models
def loadpickles(filename):
    with open(filename, 'rb') as f:
            model = pickle.load(f)
    return model

def get_code(d,modelparam):
    for x in d:
        y=d[x]
        if(y==modelparam):
            return x
    return 1

def get_average(f,choice):
    sum=0
    for i in range(3):
      sum=sum + f[i]['day'][choice]
    #   print(f[i]['day']['avgtemp_c'])
    value=sum/3
    return value

def predict_crop_for_each_day(f,scalerrf,model):
    crops=[]
    for i in range(3):
        temp=f[i]['day']['avgtemp_c']
        rain=f[i]['day']['totalprecip_mm']
        hum=f[i]['day']['avghumidity']
        x1=np.array([temp,hum,(i*100*rain+100)])
        newx1=scalerrf.transform(x1.reshape(1,-1))
        crops.append(model.predict(newx1))
    return crops

# predicting yield from crop, season, mapmyindia api data and user input
def prediction_yield(model_yield,data,area=1254, district='NICOBARS',crop='Arecanut', season='Kharif     ', state='Andaman and Nicobar Islands'):
    
    print(crop)
    
    column_names=['State_Name','District_Name','Season','Crop','Area','Production']

    # creating a dictionary of category codes and the value
    d_state = dict(enumerate(data['State_Name'].astype('category').cat.categories))
    d_district = dict(enumerate(data['District_Name'].astype('category').cat.categories))
    d_season = dict(enumerate(data['Season'].astype('category').cat.categories))
    d_crop = dict(enumerate(data['Crop'].astype('category').cat.categories))
    
    #finding the corresponding codes for user input
    statecode=get_code(d_state,state)
    districtcode=get_code(d_district,district)
    seasoncode=get_code(d_season,season)
    cropcode=get_code(d_crop,crop)

    #loading the scaler fit on training data
    scaler=loadpickles('PickledFiles/scalergb.sav')

    #creating a vector of the input features
    x=np.array([statecode,districtcode,seasoncode,cropcode,area])

    #scaling input features
    newx=scaler.transform(x.reshape(1,-1))

    #returning prediction
    return math.exp(model_yield.predict(newx))

#crop prediction and fertiliser prediction from weather api data
def prediction_crop(model_crop,model_fert,temperature=25.567483, humidity=60.492446, rainfall=190.225784,district='Bangalore'):
    
    #loading the scaler fit on the training data
    scalerrf=loadpickles('PickledFiles/scalerrf.sav')
    
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
    # print("haha")

    #taking the average for three day forecasts
    avg_temp=get_average(f,'avgtemp_c')
    avg_rain=get_average(f,'totalprecip_mm')
    avg_hum=get_average(f,'avghumidity')

    #creating feature vector out of the forecasted averages
    x3=np.array([avg_temp, avg_hum, avg_rain+5]) #adding a small smoothing parameter for 0 rainfall
    # print(x3)
    #scale the input features
    newx=scalerrf.transform(x3.reshape(1,-1))

    avg_crop=model_crop.predict(newx)
    
    all_crops=predict_crop_for_each_day(f,scalerrf,model_crop)

    all_crops.append(avg_crop)
    

    #creating a feature vector of temp and himidity for the fertiliser model
    x2=np.array([temperature, humidity])

    #loading the dictionary that maps fertliser labels to fertiliser names
    d=loadpickles('PickledFiles/dict.pkl')

    #return crop prediction and fertiliser prediction

    return np.unique(all_crops), d[model_fert.predict(x2.reshape(1,-1))[0]]



    




    
    



    
    