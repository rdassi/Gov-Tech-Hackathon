import numpy as np
import pickle
import geocoder
import requests
import pandas as pd
import time
import predict as p
from decouple import config
import base64
from PIL import Image
import io
from io import BytesIO
from io import StringIO

def get_state_and_district():
    #get the latitude and logitude corresponding to the user's IP address
    geocodeobj = geocoder.ip('me')
    print(geocodeobj.latlng)

    lat=geocodeobj.latlng[0]
    longg=geocodeobj.latlng[1]

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
    return state,district


def get_fert_composition(fert,collection):
    result= {"Fertilizer Name": fert}
    finds=collection.find_one(result)
    N=finds['Nitrogen']
    P=finds['Phosphorous']
    K=finds['Potassium']
    return N,P,K


def get_seasons():
    #get current month
    month=time.strftime("%m") 
    # print(month)

    #dictionary that maps seasons to months
    seasons={'Kharif     ': ['7', '8', '9', '10'],
            'Autumn     ': ['9', '10', '11'],
            'Summer     ': ['3', '4', '5', '6'],
            'Winter     ': ['12','1','2'],
            'Rabi       ': ['10','11','12','1','2','3']}
            # 'Whole Year ': ['1','2','3', '4', '5', '6','7', '8', '9', '10','11','12']}

    #pick all seasons for the current month
    s=[]
    for key,value in seasons.items():
        # print(value)
        for val in value:
            if(val==month):
                s.append(key)
                break

    s.append('Whole Year ')
    return s

def pred_yield_helper(df,model,crops,area,state,district):
    seasons=get_seasons()
    pred=[]
    for crop in crops:
        #convert the crop to proper case for the yield prediction model
        cropnow=crop[0].upper()+crop[1:]
        print(cropnow)
        # print(seasons)
        #store the yield prediction for each season in a list
        predictions=[]
        for season in seasons:
            # print(season)
            predictions.append(p.prediction_yield(model,df,area=area,season=season,crop=cropnow,state=state,district=district.upper()))
        
        print(predictions)
        pred.append(sum(predictions)/len(predictions))
    return pred


def crop_fert_details(mdbcollection):
    mdbcursor=mdbcollection.find()
    items_list=[]
    for val in mdbcursor:
        bin_img=val['ImageID']
        data = io.BytesIO(bin_img)
        image = Image.open(data)
        image.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        # print(encoded_img_data)
        img_data=encoded_img_data.decode('ascii')
        
        items_list.append({'img_data':img_data,'desc':val['desc'],'id':val['id']})
    return items_list