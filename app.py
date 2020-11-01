# Import libraries
import sys
import json
# from flask_cors import CORS
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import os
import predict as p

# Load the model


app = Flask(__name__, static_url_path='/static')
model_yield= p.loadModel('model.pkl')
model_rf=p.loadModel('modelrf.pkl')
#to resolve CORS error
# CORS(app)





# model = pickle.load(open('model.pkl','rb'))

@app.route('/index',methods=['POST','GET'])
def predict():
   
    # Make prediction using model loaded from disk as per the data.
    crop=p.prediction_crop(model_rf)
    cropnow=crop[0][0].upper()+crop[0][1:]
    predictiony = p.prediction_yield(model_yield,crop=cropnow)
    N,P,K,pH,soil_moisture=p.fert_pred(cropnow)
    # Take the first value of prediction
    return render_template("index.html", prediction= predictiony[0],crop=cropnow,N=N,P=P,K=K,pH=pH,soil_moisture=soil_moisture)

if __name__ == "__main__":
    #run the app, set debug=True during testing
    app.run(debug=True)


