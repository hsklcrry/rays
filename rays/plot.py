
import math
import matplotlib.pyplot as plt

results = [(1.9244811534881592, 20, 211),
 (1.9738426208496094, 21, 215),
 (0.33110857009887695, 11, 70),
 (0.5007197856903076, 13, 91),
 (1.0813584327697754, 15, 116),
 (1.5010502338409424, 19, 178),
 (2.655071973800659, 23, 256),
 (3.4900619983673096, 25, 301),
 (4.311450958251953, 27, 350),
 (6.799299240112305, 31, 460),
 (10.989641666412354, 36, 620),
 (16.79231333732605, 41, 805),
 (24.797593355178833, 46, 1015),
 (35.72976565361023, 51, 1250),
 (47.03675723075867, 56, 1510),
 (146.80444526672363, 76, 2800),
]

results2 = []
for x in results:
    results2.append((x[1] + x[2], x[0]))

results.sort(key=lambda x: x[1])
results2.sort(key=lambda x: x[1])

intersections = []
time = []
edges = []

for x in results:
    intersections.append(x[2])
    time.append(x[0])
    edges.append(x[1])

plt.plot(intersections, time)

plt.ylabel('some numbers')

plt.show()


time = []
ePlusI = []

for x in results2:
    ePlusI.append(x[0])
    time.append(x[1])

plt.plot(ePlusI, time)

plt.ylabel('time(e + i)')

plt.show()

r = []
for i in range(len(results)):
    r.append(1000*results2[i][1] / (results2[i][0]*math.log(results2[i][0])*math.log(results2[i][0])))

logn = list(map(lambda x: math.log(x), ePlusI))

plt.plot(ePlusI, r, 'r')
plt.plot(ePlusI, logn, 'g')
plt.show()
plt.plot(ePlusI, [10*a/b for a,b in zip(r,logn)])


