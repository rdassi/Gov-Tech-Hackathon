#importing
import numpy as np
import pickle
import pandas as pd
import math
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor

import pickle

# add meaning of default values
def prediction_yield(model,area=1254, district='NICOBARS',crop='Arecanut', season='Kharif     ', state='Andaman and Nicobar Islands'):
    print(crop)
    data=pd.read_csv('indiaselected.csv')
    # data=data.drop(['Crop_Year'],axis=1)
    # categorical_columns=['State_Name','District_Name','Season','Crop']
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
    # scaler = StandardScaler()
    # result=data1.to_numpy()
    # X=[]
    # for ele in result:
    #     X.append(ele[:-1])


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
    # flag=0
    for x in d_crop:
        y=d_crop[x]
        if(y==crop):
            cropcode=x
            # flag=1

    # if(flag==0):
    #     crop='Arecanut'
    #     for x in d_crop:
    #         y=d_crop[x]
    #         if(y==crop):
    #             cropcode=x

    
    
    scaler=pickle.load(open('scalergb.sav','rb'))
    x=np.array([statecode,districtcode,seasoncode,cropcode,area])
    newx=scaler.transform(x.reshape(1,-1))

    return math.exp(model.predict(newx))

def prediction_crop(model,model2,temperature=25.567483, humidity=60.492446, rainfall=190.225784,district='Bangalore'):
    print(district)
    response = requests.get("http://api.weatherapi.com/v1/forecast.json?key=6e1498be712f43a081f200018203110&q="+district+"&days=10",)
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

    x=np.array([temperature, humidity, 120])
    print(x)
    scalerrf=pickle.load(open('scalerrf.sav','rb'))
    newx=scalerrf.transform(x.reshape(1,-1))
    x2=np.array([temperature, humidity])
    d=pickle.load(open('dict.pkl','rb'))
    return model.predict(newx), d[model2.predict(x2.reshape(1,-1))[0]]

def loadModel(filename):
    with open(filename, 'rb') as f:
            model = pickle.load(f)
    return model
    
# def fert_pred(name,model):
    
#     # root_path='FertilizerData.csv'
#     # df=pd.read_csv(root_path)
    
#     # x=df.loc[df['Crop'] == name.lower()]
#     # z1=x['N'].values
#     # # print(z[0],"haha")
#     # z2=x['P'].values
#     # z3=x['K'].values
#     # z4=x['pH'].values
#     # z5=x['soil_moisture'].values
#     return z1[0],z2[0],z3[0],z4[0],z5[0]


# def optimise(crop,district='NICOBARS',area=1254):
#     commoncrops=['Rice', 'Maize', 'Blackgram', 'Lentil', 'Banana', 'Mango',
#        'Grapes', 'Apple', 'Orange', 'Papaya', 'Jute', 'Coffee']

#     yieldfile=pd.read_csv('apy.csv')
#     fertilisers=pd.read_csv('FertilizerData.csv')
#     districtcrops=yieldfile[yieldfile['District_Name']==district].reset_index(drop=True)
#     cropsbyarea=districtcrops[districtcrops['Area']<=area].reset_index(drop=True)
#     k=0
#     for crops in cropsbyarea['Crop']:
#         # cropsbyarea[k]['Production']
#         row=fertilisers[fertilisers['Crop']==crops.lower()]
#         n=row['N']
#         p=row['P']
#         k=row['K']
#         total=n+p+k
#         print(total,n,p,k,row)
#         k+=1
#         break



    
    



    
    