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

        #Initializing Raw EEG array and time array
        self.raw_eeg_arr = []
        self.time_arr = []

        #utilizing built in thinkGearConnector sdk, enable raw output
        self.tn.write('{"enableRawOutput": true, "format": "Json"}'.encode('ascii'))

        #Marking beginning time for counter
        self.start = time.perf_counter()
        
        # Initializig  default save length for saveData function
        self.saveLen = 1000
    def clearData(self):
        self.raw_eeg_arr = []
    def getData(self, num):
        #Gathering Data from Headset for 1 seconds
        self.start = time.perf_counter()
        
        #Intiialize row array
        row = []
        
        #In 5 Second Intervals, load in rawEeg data from headset, decode it, and save it to self.raw_eeg_arr
        while (time.perf_counter() - self.start) <= 5:
            line = self.tn.read_until(b'\r').decode('ascii')
            dict = json.loads(str(line))
            #if loaded line is less than 20 characters in length, ie. if the headset is sending raw Eeg values
            if len(line) < 20:
                row.append(dict['rawEeg'])
            else:
                print(dict)
                
        #Capture the least possible amount of headset transmission through the course of the 5 second interval
        #variable later used for saving data to a constant length
        if len(row) < self.saveLen:
            self.saveLen = len(row)
        
        self.raw_eeg_arr.append([num]+row)
        
    #Save Data to csv format in file 'data.csv'
    def saveData(self):
        #Going row by row of self.raw_eeg_arr, append to the 'data.csv' file
        with open('data.csv', 'a+', newline='\n') as write_obj:
            csv_writer = writer(write_obj)
            for row in self.raw_eeg_arr:
                csv_writer.writerow(row[:self.saveLen+1])
    
    #Plotting a graph of Time vs. Eeg Values
    def graphData(self):
        plt.plot(self.time_arr,self.raw_eeg_arr)
        plt.ylabel("raw Eeg Values")
        plt.xlabel("time")

        plt.show()


