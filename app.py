# Import libraries
import sys
import json
# from flask_cors import CORS
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import os
import predict as p
from sklearn.ensemble import GradientBoostingRegressor

# Load the model
model_yield= p.loadModel('modelgb.pkl')
model_rf=p.loadModel('modelrf.pkl')

app = Flask(__name__, static_url_path='/static')

#to resolve CORS error
# CORS(app)


@app.route('/index',methods=['POST','GET'])
def predict():

    
    # Make prediction using model loaded from disk as per the data.
    crop=p.prediction_crop(model_rf)
    cropnow=crop[0][0].upper()+crop[0][1:]
    print(cropnow)
    predictiony = p.prediction_yield(model_yield,crop=cropnow)
    N,P,K,pH,soil_moisture=p.fert_pred(cropnow)
    # p.optimise(cropnow)
    # Take the first value of prediction
    return render_template("index.html", prediction= predictiony,crop=cropnow,N=N,P=P,K=K,pH=pH,soil_moisture=soil_moisture)

if __name__ == "__main__":
    #run the app, set debug=True during testing
    app.run(debug=True)


