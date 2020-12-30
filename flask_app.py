# Import libraries
import sys
import json
from flask import Flask, request, jsonify, render_template, url_for, redirect, make_response, g, session
from flask_sqlalchemy import SQLAlchemy 
from  werkzeug.security import generate_password_hash, check_password_hash 
from functools import wraps 
import predict as p
from decouple import config
import pymongo
from pymongo import MongoClient 
import farmer_functions as ff
# import firebase_admin
# from firebase_admin import credentials,auth
import pandas as pd 
from datetime import datetime, timedelta 
import pyrebase
# cred = credentials.Certificate("farmers-app-2626e-firebase-adminsdk-gbudd-bee616ba3a.json")
# firebase_admin.initialize_app(cred)
firebaseConfig ={
    "apiKey": config("fb_apiKey"),
    "authDomain": config("fb_authDomain"),
    "databaseURL": config("fb_databaseURL"),
    "projectId": config("fb_projectId"),
    "storageBucket": config("fb_storageBucket"),
    "messagingSenderId": config("fb_messagingSenderId"),
    "appId": config("fb_appId"),
    "measurementId": config("fb_measurementId")

}
firebase =pyrebase.initialize_app(firebaseConfig)

fdb=firebase.database()

#getting the cluster from the database url
cluster=MongoClient(config('db_url'))

#accessing the fertliser data
dbm=cluster["FertilizerData"]

#getting the subset that corresponds to querying 
collection=dbm["FertilizerQueryData"]
collection2=dbm["IndiaSelect"]

# Load the models
model_yield= p.loadpickles('PickledFiles/modelgb.pkl')
model_rf=p.loadpickles('PickledFiles/modelrf.pkl')
model_fert=p.loadpickles('PickledFiles/modelfert.pkl')

#app instance
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = config('secret_flask_key')
app.config['SQLALCHEMY_DATABASE_URI'] = config('PSQL_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#allows cross origin requests for location
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app) 
   
# Database ORMs 
class User(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(100)) 
    phone = db.Column(db.String(10), unique = True) 
    password = db.Column(db.String(128)) 
    area = db.Column(db.Float)
    soil_type=db.Column(db.String(8))
    state =db.Column(db.String(50))
    district = db.Column(db.String(50))

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        
        user = User.query.filter_by(id = session['user_id']).first()  
        g.user = user

# for the / route, render index.html template under two conditions
@app.route('/index',methods=['POST','GET'])
def location():
    if not g.user:
        return redirect(url_for('login'))
    
    df = pd.DataFrame(list(collection2.find()))
    # print(df)
    
    #get current user's details
    state = g.user.state
    area = g.user.area
    district = g.user.district

    #predicting the crop using the district as input to weather api, which further gives weather input features to model,
    #and also using weather data to predict fertiliser
    crops,fert=p.prediction_crop(model_crop=model_rf,model_fert=model_fert,district=district)
    print(crops)

    #use the predicted fertiliser to query npk values
   
    N,P,K=ff.get_fert_composition(fert,collection)

    #predicting yield for each crop
    crop_yields=ff.pred_yield_helper(df,model_yield,crops=crops,area=area,state=state,district=district)

    #get current timestamp
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    for i in range(len(crops)):
        #adding some random data to firebase db just to see if it is working
        fbdata= {'timestamp':dt_string,'crop':crops[i],'yield':crop_yields[i],'N':N,'P':P,'K':K,'Fertiliser':fert}
        fdb.child("users").child(g.user.id).push(fbdata)

    #render template with predicted values (average yield, crop, NPK values, fertliser name)
    return render_template("index.html",yields=crop_yields,crop=crops,fertiliser=fert,N=N,P=P,K=K)
    

@app.route('/login', methods =['POST','GET']) 
def login(): 
    if request.method=='POST':

        session.pop('user_id', None)

        # creates dictionary of form data 
        auth = request.form 
    
        if not auth or not auth.get('phone') or not auth.get('password'): 
            # returns 401 if any phone or / and password is missing 
            return make_response( 
                'Could not verify', 
                401, 
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
            ) 
    
        user = User.query.filter_by(phone = auth.get('phone')).first() 
    
        if not user: 
            
            return redirect(url_for("signup"))
    
        if check_password_hash(user.password, auth.get('password')): 
            
            session['user_id'] = user.id
    
            # return make_response(jsonify({'token' : token.decode('UTF-8')}), 201) 
            return redirect(url_for("profile"))
        # returns 403 if password is wrong 
        return redirect(url_for('login'))

    return render_template("login.html")
   
# signup route 
@app.route('/signup', methods =['POST','GET']) 
def signup(): 

    if request.method=='POST':
        session.pop('user_id', None)
    # creates a dictionary of the form data 
        data = request.form 
        state, district=ff.get_state_and_district()
        # gets name, phone and password 
        name, phone, area, soil = data.get('name'), data.get('phone') , data.get('area'), data.get('soil')
        password = data.get('password') 
    
        # checking for existing user 
        user = User.query.filter_by(phone = phone).first() 
        if not user: 
            # database ORM object 
            user = User( 
                name = name, 
                phone = phone, 
                password = generate_password_hash(password),
                area = area,
                state = state,
                district = district,
                soil_type = soil
            ) 
            # insert user 
            db.session.add(user) 
            db.session.commit() 
            session['user_id'] = user.id
            return redirect(url_for("profile"))
        else: 
            
            return redirect(url_for("login"))
    return render_template("phone_verification.html")

@app.route('/',methods=['POST','GET'])
def startfunc():
    return render_template("landing.html")



@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

@app.route('/set_values',methods =['POST','GET'])
def setuserparamsfunc():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form.get('area'):
            updateduser = User.query.filter_by(id=g.user.id).update(dict(area=request.form.get('area')))
            db.session.commit()
        if request.form.get('soil'):
            updateduser = User.query.filter_by(id=g.user.id).update(dict(soil_type=request.form.get('soil')))
            db.session.commit()
        # return redirect(url_for('setuserparamsfunc'))
        
    return render_template("update_values.html")

@app.route('/past_rec',methods =['POST','GET'])
def past_rec():
    if not g.user:
        return redirect(url_for('login'))
    people = fdb.child("users").get()
    for person in people.each():
        print(person.key())
        if(person.key()==str(g.user.id)):
            recs=person.val()
    return render_template("past_rec.html",recs=recs)

@app.route('/view_crops',methods =['POST','GET'])
def view_crops():
    if not g.user:
        return redirect(url_for('login'))
    
    crops=['fskNFs','afjBJKSDf']
    return render_template("view_crops.html",crops=crops)

@app.route('/view_ferts',methods =['POST','GET'])
def view_ferts():
    if not g.user:
        return redirect(url_for('login'))
    
    ferts=['haha','asdhka']
    return render_template("view_ferts.html",ferts=ferts)

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect(url_for('startfunc'))

if __name__ == "__main__":
    #run the app, set debug=True during testing
    app.run(debug=True)


