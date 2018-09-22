
import math
import matplotlib.pyplot as plt

results = [
 (0.15641021728515625, 5, 31),
 (0.5766420364379883, 10, 66),
 (0.9263088703155518, 12, 87),
 (1.309218406677246, 14, 112),
 (1.8713598251342773, 16, 141),
 (2.6588542461395264, 18, 174),
 (3.7097582817077637, 20, 211),
 (4.895186424255371, 22, 252),
 (6.538226842880249, 24, 297),
 (8.849840641021729, 26, 346),
 (10.962988376617432, 28, 399),
 (13.368473768234253, 30, 456),
 (50.5209743976593, 45, 925)
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


