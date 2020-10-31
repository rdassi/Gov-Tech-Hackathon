# Import libraries
import sys
import json
# from shapely.geometry import shape, Point 
# from flask_cors import CORS
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import os
import predict as p
# from http.server import BaseHTTPRequestHandler, HTTPServer
# PORT_NUMBER = int(os.environ.get('PORT', 8084))

# Load the model


app = Flask(__name__, static_url_path='/static')
model= p.loadModel()
#to resolve CORS error
# CORS(app)

# @app.route("/index")
# def helloWorld():
#   return "Hello, cross-origin-world!"
#!/usr/bin/python



# model = pickle.load(open('model.pkl','rb'))

@app.route('/index',methods=['POST','GET'])
def predict():
    # # Get the data from the POST request.
    # data = request.get_json(force=True)
    # Make prediction using model loaded from disk as per the data.
    prediction = p.prediction(model)
    # Take the first value of prediction
    return render_template("index.html", prediction= prediction)

if __name__ == "__main__":
    #run the app, set debug=True during testing
    app.run(debug=True,)


# # HTTPRequestHandler class
# class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
#   # GET
#   def do_HEAD(self):
#         # Send response status code
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#         return
#   # GET
#   def do_GET(self):
#         # Send response status code
#         self.send_response(200)
 
#         # Send headers
#         self.send_header('Content-type','text/html')
#         self.end_headers()
 
#         # Send message back to client
#         message = "Hello world!"
#         # Write content as utf-8 data
#         self.wfile.write(bytes(message, "utf8"))
#         return
 
# def run():
#   print('starting server...')
 
#   # Server settings
#   # Choose port 8080, for port 80, which is normally used for a http server, you need root access
#   server_address = ('0.0.0.0', PORT_NUMBER)
#   httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
#   print('running server...')
#   httpd.serve_forever()
  
# run()


