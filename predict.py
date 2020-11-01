#importing
import numpy as np
import pickle
import pandas as pd
import requests
from sklearn.preprocessing import StandardScaler



# add meaning of default values
def prediction_yield(model,area=1254, district='NICOBARS',crop='Arecanut', season='Kharif     ', state='Andaman and Nicobar Islands'):
    print(crop)
    data=pd.read_csv('apy.csv')
    data=data.drop(['Crop_Year'],axis=1)
    categorical_columns=['State_Name','District_Name','Season','Crop']
    data1=pd.DataFrame()
    data1['State_Name']=data['State_Name'].astype('category').cat.codes
    data1['District_Name']=data['District_Name'].astype('category').cat.codes
    data1['Season']=data['Season'].astype('category').cat.codes
    data1['Crop']=data['Crop'].astype('category').cat.codes
# data['Crop_Year']=data['Crop_Year'].astype('category')

    data1['Area']=data['Area']
    data1['Production']=data['Production']
    d_state = dict(enumerate(data['State_Name'].astype('category').cat.categories))
    d_district = dict(enumerate(data['District_Name'].astype('category').cat.categories))
    d_season = dict(enumerate(data['Season'].astype('category').cat.categories))
    d_crop = dict(enumerate(data['Crop'].astype('category').cat.categories))
    scaler = StandardScaler()
    result=data1.to_numpy()
    X=[]
    for ele in result:
        X.append(ele[:-1])
    X1=scaler.fit_transform(X)


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
    
    x=np.array([statecode,districtcode,seasoncode,cropcode,1254.0])
    newx=scaler.transform(x.reshape(1,-1))

    return model.predict(newx)

def prediction_crop(model,temperature=25.567483, humidity=60.492446, rainfall=190.225784):
    response = requests.get("http://api.weatherapi.com/v1/forecast.json?key=6e1498be712f43a081f200018203110&q=Bangalore&days=10",)
    print(response.status_code)

    x=response.json()
    y=pd.DataFrame.from_records(x)
    z=y['forecastday':'name']
    f=z['forecast']['forecastday']

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

    x=np.array([temperature, humidity, rainfall])

    return model.predict(x.reshape(1,-1))

def loadModel(filename):
    with open(filename, 'rb') as f:
            model = pickle.load(f)
    return model
    