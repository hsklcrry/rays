# -*- coding: utf-8 -*-
"""
Created on Sat May 26 19:22:20 2018

@author: ernst
-------------------------------
"""

import avl
import avl_b
from classes import Edge, Pt, BLACK, Ray, EPS

import time


intersections = dict()  # avl.Leaf()
q = dict()
pts = dict()    # ключ - луч из 0. Значения - точки на этом луче,
# упорядоченные по расстоянию от 0
s = avl.Leaf()  # события

tau = avl_b.LeafN()

# ВХОДНЫЕ ДАННЫЕ
input_edges = [Edge.fromCoordinates(3.0, 1.0, 4.0, 0.0, color=BLACK),
               Edge.fromCoordinates(0.0, 4.0, 1.0, 3.0, color=BLACK),
               Edge.fromCoordinates(4.0, 1.0, 1.0, 4.0, color=BLACK),
               Edge.fromCoordinates(6.0, 5.0, 5.0, 6.0, color=BLACK),
               Edge.fromCoordinates(2.0, 0.0, 1.0, 2.0, color=BLACK)
               ]

for i in range(10, 23):
    input_edges.append(Edge.fromCoordinates(i + 1.0, 0.0,
                                            i + 1.0, 1.0, color=BLACK))
    # input_edges.append(Edge.fromCoordinates(i + 0.5, 20.0,
    #                                        i + 1.0, 20.0, color=BLACK))


edges = input_edges.copy()
rays = dict()

R = 1000.0

for e in edges:
    s = s.insert(e.left)
    s = s.insert(e.right)

# добавляем отрезки из начала, попутно создаём лучи
for v in s:
    e = Edge(Pt(0.0, 0.0), Pt.mul(R, v), isRay=True)
    r = Ray.fromEdge(e)
    if (r not in pts):
        pts[r] = avl.Leaf()
        edges.append(e)
    rays[e] = avl.Leaf()


edges.sort(key=lambda x: x.left)  # n ln n
# print(edges)

for e in edges:
    if q.get(e.left) is None:
        q[e.left] = set()
    if q.get(e.right) is None:
        q[e.right] = set()
    # Edge.event = e.left
    q[e.left].add(e)
    s = s.insert(e.left)
    s = s.insert(e.right)


def HandleEvent(p):
    # p.color = BLACK
    Edge.event = p
    intersections[p] = avl.Leaf()
    # print('################################################################')
#    print('p = {pt}'.format(pt=p))
    global tau
    global q

    # выбрали высоту
    ###########################################################
    # step 1
    Edge.height = p.y
    U = avl_b.LeafN()
    if q.get(p) is not None:
        U = U.update(q[p])

    ###########################################################
    # step 2
    # print('Height = {ht}'.format(ht=float(Edge.height)))
    c = avl_b.LeafN()
    low = avl_b.LeafN()
    for e in tau:
        # по сложности не получается
        if e.containPt(p):
#            print('{e} contains the point'.format(e=e))
            if e.isL():
#                print('new one in low is {e}'.format(e=e))
                low = low.insert(e)
            else:
                if e.isC():
#                    print('new one in mid is {e}'.format(e=e))
                    c = c.insert(e)

#    print('c = {c}'.format(c=c))
#    print('low = {c}'.format(c=low))
#    print('tau = {c}'.format(c=tau))
    ###########################################################
    # steps 3, 4
#    print('UnuionUCL = ({un}, {cn}, {ln})'.format(
#       un=len(U),
#       cn=len(c),
#       ln=len(low)))
#    print('#####')
    if len(U) + len(c) + len(low) > 1:
        intersections[p] = intersections[p].update(U, c, low)
    ###########################################################
    # step 5
    Edge.isInserting = False
    tau = tau.difference(c, low)
    ###########################################################
    # step 6
    Edge.isInserting = True
    for e in U:
        try:
            tau = tau.insert(e)
        except(Exception):
            # print('exc')
            pass
    for e in c:
        try:
            tau = tau.insert(e)
        except(Exception):
            # print('exc')
            pass
    ###########################################################
    # step 8...
    # uc = c.copy() - ошибка. Порядок рёбер в C инвертирован
    uc = avl_b.LeafN().update(c)
    for e in U:
        try:
            uc = uc.insert(e)
        except Exception as e:
            # print('exc at uc = {e}'.format(e=e))
            pass
    Edge.height = p.y
    # uc = c.update(U)
    # if e.isRay:
    #    rays[e] = rays[e].update(tau)
    # tau1 = tau  # avl.Leaf().update(tau)
    if len(uc) == 0:
#        print('low == {l1}'.format(l1=low))
        try:
            s1 = tau.getPrev(low.findmin().key)
            s2 = tau.getNext(low.findmax().key)
#            print('FNE1({s1}, {s2})'.format(s1=s1, s2=s2))
            findNewEvent(s1, s2, p)
        except AttributeError as a:
#            print('1 -- ' + str(a), )
            pass
    else:
        try:
            s1 = uc.findmin().key
            s2 = tau.getPrev(s1)
#            print('FNE2({s1}, {s2})'.format(s1=s1, s2=s2))
            findNewEvent(s1, s2, p)
        except AttributeError as a:
#            print('2 --' + str(a))
            pass
        try:
            s1 = uc.findmax().key
            tau1 = tau
            s2 = tau.getNext(s1)
            if tau1 != tau:
                raise Exception('OofFNE3')
#            print('FNE3({s1}, {s2})'.format(s1=s1, s2=s2))
            findNewEvent(s1, s2, p)
        except AttributeError as a:
#            print('3 --' + str(a))
            pass
    ###########################################################
    return


def findNewEvent(s1, s2, p):
    global intersections
    global s
    if s1.isRay and s2.isRay:
        return
    if s1.isIntersect(s2):
        i = s1.getIntersection(s2)
        if i > p:
#            print('    {s1} intersects {s2}'.format(s1=s1, s2=s2))
#            print('    new intersection {pt}'.format(pt=i))
            if intersections.get(i) is None:
                intersections[i] = avl.Leaf()
            Edge.event = i
            intersections[i] = intersections[i].update([s1, s2])
            Edge.event = p
            s = s.insert(i)
    return


start = time.time()
while len(s) > 0:
    v = s.findmin().key
    s = s.removemin()
    start1 = time.time()
    print(v)
    HandleEvent(v)
    end1 = time.time()
#    print('ELAPSED TIME: {t}'.format(t=end1 - start1))

end = time.time()

Pt.__lt__ = Pt.cmpByDistance  # сравниваем по расстоянию

for x in intersections:
    if x != Pt(0, 0, BLACK) and x != Pt(0, 0):
        r = Ray(x)
#        print('p = {pt} r = {r}'.format(pt=x, r=r))
        if (r not in pts):
            pts[r] = avl.Leaf()
        pts[r] = pts[r].insert(x)

print('--------------------------------------------------')
print('Output:')
visible = set()
for ray in pts:
#    print('ray target is {t}'.format(t=ray.target))
    nearestPt = pts[ray].findmin().key
#    print('nearest Point is {pt}'.format(pt=nearestPt))
    # print(nearestPt, ':')
#    print('nearest Point color is {col}'.format(col=nearestPt.color))
    if nearestPt.color == BLACK:
        # если ближайшая точка граничная, то смотрим следующую
        for e in intersections[nearestPt]:
            if not e.isRay:
#                print('1. edge is {e}'.format(e=e))
                visible.add(e)
        nextPt = pts[ray].getNext(nearestPt)
#        print('next pt is {pt} and has color {color}'.format(pt=nextPt,
#              color=nextPt.color))
        if nextPt.color != BLACK:
            # если следующая точка не граничная
            for e in intersections[nextPt]:
                if not e.isRay:
#                    print('2. edge is {e}'.format(e=e))
                    visible.add(e)
    else:
        #  иначе
        for e in intersections[nearestPt]:
            if not e.isRay:
#                print('3. edge is {e}'.format(e=e))
                visible.add(e)

print('Visible edges are: {vis}'.format(vis=visible))
print('ELAPSED TIME: {t}. e = {l}, i = {i}'.format(
        t=end - start,
        l=len(input_edges), 
        i=len(intersections)))
#results.append((end - start, len(input_edges), len(intersections)))
