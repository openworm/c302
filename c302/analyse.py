import sys
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


fig = plt.figure(facecolor='#FFFFFF', edgecolor='#FFFFFF')
p = fig.add_subplot(111)


dat_file = sys.argv[1]

traces = open(dat_file,'r')
volts = {}

# Very inefficient...
for line in traces:
    if not line.strip().startswith('#'):
        points = line.split()
        for i in range(len(points)):
            if not volts.has_key(i):
                volts[i] = []
            volts[i].append(float(points[i])+0.0020*i)

for cell_index in volts.keys():
    if cell_index <=302:
        if cell_index >0:
            p.plot(volts[0], volts[cell_index])
        
plt.show()



