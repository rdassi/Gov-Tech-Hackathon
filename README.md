# Gov-Tech-Hackathon
AI-based crop recommendation system

## Overview

### This project uses two external APIs: <br>
1. mapmyindia - to get district and state names from the latitude and longitude provided <br>
2. weather - to get humidity, temperature, rainfall using the district provided <br>

### It then uses 3 models: <br>
1. Crop prediction - uses weather api and returns best crop (Random Forest Classification)<br>
2. Fertiliser prediction - uses weather api and returns fertiliser name (K Nearest Neighbours Classification) <br>
3. Crop yield prediction - uses crop predicted, state, district, season, area of farm to predict the yield (Gradient Boosted Regression) <br>

### Database Usage:<br>
It stores the training dataset for crop yield prediction as well as the fertiliser names and corresponding npk values in two separate collections. <br>
The mongoDB database is used for two purposes: <br>
1. It uses the training dataset to obtain the label enconding of the user inputs during run-time <br>
2. Uses the fertiliser name predicted to query the corresponding NPK values <br>
