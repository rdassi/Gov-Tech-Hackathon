#importing
import numpy as np
import pickle


# add meaning of default values
def prediction(area=306, district=471, year=17, crop=95, season=3, state=32, model):
    x=np.array([state, district, year, season, crop, area])
    return (model.predict(x.reshape(1,-1)))

def loadModel():
    with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
    return model
    