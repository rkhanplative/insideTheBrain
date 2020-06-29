import numpy
a = numpy.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
numpy.savetxt("test.csv", a, delimiter=",")

import headset

test = headset.headset()

test.getData(69)
test.saveData()