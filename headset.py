import telnetlib
import time
import numpy as np
import json.scanner
import matplotlib.pyplot as plt
from csv import writer

class headset(object):
    def __init__(self):
        #Connect to Minwave device at localhost throught port 13854
        self.tn = telnetlib.Telnet('127.0.0.1',13854)

        #Initializing Raw EEG array
        self.raw_eeg_arr = []

        #utilizing built in thinkGearConnector sdk, enable raw output
        self.tn.write('{"enableRawOutput": true, "format": "Json"}'.encode('ascii'))

        #Marking beginning time for counter
        self.start = time.perf_counter()

        # Initializig  default save length for saveData function        
        self.label = ""
        
        self.labels=["yes","no"]
    def getData(self,label):
        self.label = label
        self.start = time.perf_counter()
        #In 5 Second Intervals, load in rawEeg data from headset, decode it, and save it to self.raw_eeg_arr
        while (time.perf_counter() - self.start) <= 5:
            line = self.tn.read_until(b'\r').decode('ascii')
            dict = json.loads(str(line))
            #if loaded line is less than 20 characters in length, ie. if the headset is sending raw Eeg values
            if len(line) > 30:
                powerDict = dict["eegPower"]
                with open('data/data.csv', 'a+', newline='\n') as write_obj:
                    csv_writer = writer(write_obj)
                    csv_writer.writerow([self.labels.index(self.label),
                                        time.perf_counter() - self.start,
                                        powerDict["delta"],
                                        powerDict["theta"],
                                        powerDict["lowAlpha"],
                                        powerDict["highAlpha"],
                                        powerDict["lowBeta"],
                                        powerDict["highBeta"],
                                        powerDict["lowGamma"],
                                        powerDict["highGamma"]])
    #Returns relative connectivity of headset
    def getConnectivity(self):
        self.start = time.perf_counter()

        while (time.perf_counter() - self.start) <= 5:
            line = self.tn.read_until(b'\r').decode('ascii')
            dict = json.loads(str(line))

            if len(line) > 25:
                self.connection = dict['poorSignalLevel']

        if self.connection == 0: return "Strong Connection"
        elif self.connection > 0 and self.connection < 200: return "Okay connection"
        else: return "Poor Connection"

