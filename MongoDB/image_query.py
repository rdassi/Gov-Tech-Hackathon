import pymongo
from PIL import Image
from pathlib import Path
import json
import io
from io import BytesIO
from io import StringIO
from bson.binary import Binary as Binary
path = Path("/Users/neelbhandari/Downloads/Images/jute.jpeg")
img  =Image.open(path)

#MongoDB takes image data through bytes as a Binary object
buf = BytesIO()
img.save(buf, 'jpeg')
buf.seek(0)
image_bytes = buf.read()
Binary_image_file = Binary(image_bytes)

#Pushing data
from pymongo import MongoClient 
cluster=MongoClient("mongodb+srv://neelb:Fertilizer123@fertilizer.244tu.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=cluster["FertilizerData"]
collection=db["Imagecollec"]
data_img={'id':'jute','ImageID':image_bytes, 'desc': 'Jute crop grows well in rainfed, moderate, warm humid atmosphere and sunshine conditions.River basins or alluvial or loamy soils are best for jute cultivation.'}
collection.insert_one(data_img)


# QUERY IMAGES
# coll= collection.find_one({"id": 1})
# bin_img=coll['ImageID']
# image_data = io.BytesIO(bin_img)
# image = Image.open(image_data)


# bins=bin_img['ImageID']
# image_data =StringIO.StringIO(bins)
# image = Image.open(image_data)

