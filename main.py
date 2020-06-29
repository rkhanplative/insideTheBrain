from flask import Flask
from flask import render_template
import headset
import time
import random
import logging

#Establishing Global Variables
app = Flask(__name__)
Headset = headset.headset()
random_numbers = [x for x in range(1,11)]*3
random.shuffle(random_numbers)

#Cleaning up terminal output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#Main Trainig Interface
@app.route('/training/')
def training(name=None):
    return render_template('training.html',data=random_numbers)

#Background process responsible for actual capturing of headset data at same right of random numbers being displayed to screen
@app.route('/background_process/')
def train():
    time.sleep(1)
    '''
    for the 12 numbers in the given 60 seconds, 
    capture brain patterns, and save them locally (CSV format),
    to be later utilized for ML model training
    '''
    print("-"*100)
    for c, num in enumerate(random_numbers):
        Headset.getData(num)
        print('Training Progress: ['+ '-'*(c+1) + ' '*(29-c) +"] " + str(c+1)+" out of 30 tests completed")
    print("\nTraining Session Complete.")
    Headset.saveData()
    Headset.clearData()
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)