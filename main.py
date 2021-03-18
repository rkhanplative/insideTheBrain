from flask import Flask
from flask import render_template
from django.shortcuts import render
import headset
import time
import random
import logging
import json

#Establishing Global Variables
app = Flask(__name__)
Headset = headset.headset()

#random numbers that are displayed to screen for training
labels = ['yes','no'] * 15

#Cleaning up terminal output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#Main Training Interface
@app.route('/training/')
def training(name=None):
    return render_template ('training.html',data=labels)

#Background process responsible for actual capturing of headset data at same rate of random numbers being displayed to screen
@app.route('/background_process/')
def train():
    '''
    for the 12 numbers in the given 60 seconds, 
    capture brain patterns, and save them locally (CSV format),
    to be later utilized for ML model training
    '''
    print("-"*100)
    for c, label in enumerate(labels):
        Headset.getData(label)
        print('Training Progress: ['+ '-'*(c+1) + ' '*(29-c) +"] " + str(c+1)+" out of 30 tests completed")
    print("\nTraining Session Complete.")
    return ""

@app.route('/check_connectivity/')
def check_connectivity():
    time.sleep(1)
    print("Checking Connectivity... ")
    print(" Status: "+Headset.getConnectivity())
    return ""

if __name__ == "__main__":
    app.run(debug=True)