import headset
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

'''
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
'''
'''
test = headset.headset()
test.getConnectivity()
time.sleep(5)
test.getData("yes")
'''

fig, axs = plt.subplots(2,9)
frequencies = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'highGamma']

#time, delta, theta, lowAlpha, highAlpha, lowBeta, highBeta, lowGamma, highGamma
dataFile = np.loadtxt(open("data/data.csv", "rb"), delimiter=",", skiprows=1)
data = dataFile.T[1:]
fileLabels = dataFile.T[0]

tests = []
testLabels = []
testCaseNum = -1

def merge(list1, list2): 
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list 

averages = [[[]for y in range(0,8)] for x in range(0,2)]
for i in range(0,len(fileLabels)):
    if i == 0 or fileLabels[i] != fileLabels[i-1]:
        testCaseNum+=1
        tests.append([[],[],[],[],[],[],[],[],[]])
        testLabels.append(fileLabels[i])
    for x, dataPoint in enumerate(data.T[i]):     #Converts transpose of data matrix from np.array to list
        tests[testCaseNum][x].append(dataPoint)

for i, t in enumerate(tests):
    averageData = [(t[1][x]+t[2][x]+t[3][x]+t[4][x]+t[5][x]+t[6][x]+t[7][x]+t[8][x])/7 for x in range(0,len(t[0]))]
    if testLabels[i] == 0: #If person is thinking yes
        axs[0,0].plot(t[0],averageData)
        for x in range(2,17,2): #Even rows of axs matrix represent coordinate points for yes
            axs[0,int(x/2)].plot(t[0],t[int(x/2)])
            averages[0][int(x/2)-1]+=t[int(x/2)]
    else: #If person is thinking no
        axs[1,0].plot(t[0],averageData)
        for x in range(3,18,2): #Odd rows of axs matrix represent coordinate points for no
            axs[1,int((x-1)/2)].plot(t[0],t[int((x-1)/2)])
            averages[1][int((x-1)/2)-1]+=t[int((x-1)/2)]

for x, response in enumerate(averages):
    for y, frequency in enumerate(response):
        averages[x][y] = sum(averages[x][y])/len(averages[x][y])

for frequency, (yesAvg, noAvg) in enumerate(merge(averages[0],averages[1])):
    print("(Yes) %s %d"%(frequencies[frequency],yesAvg))
    print("(No) %s %d"%(frequencies[frequency],noAvg))

axs[0,0].set(title="Yes (Average)")
axs[1,0].set(title="No (Average)")

axs[0,1].set(title="Yes (Delta)")
axs[1,1].set(title="No (Delta)")

axs[0,2].set(title="Yes (Theta)")
axs[1,2].set(title="No (Theta)")

axs[0,3].set(title="Yes (lowAlpha)")
axs[1,3].set(title="No (lowAlpha)")

axs[0,4].set(title="Yes (highAlpha)")
axs[1,4].set(title="No (highAlpha)")

axs[0,5].set(title="Yes (lowBeta)")
axs[1,5].set(title="No (lowBeta)")

axs[0,6].set(title="Yes (highBeta)")
axs[1,6].set(title="No (highBeta)")

axs[0,7].set(title="Yes (lowGamma)")
axs[1,7].set(title="No (lowGamma)")

axs[0,8].set(title="Yes (highGamma)")
axs[1,8].set(title="No (highGamma)")

fig.text(0.5, 0.04, 'Time Elapsed', ha='center')
fig.text(0.04, 0.5, 'Frequency Strength', va='center', rotation='vertical')



fig.suptitle('Averaged EEG Data seperated by thought in 5 second intervals')
plt.show()
