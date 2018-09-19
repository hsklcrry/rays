# -*- coding: utf-8 -*-
"""
Created on Sat May 26 19:22:20 2018

@author: ernst
"""

#import avl
import avl_b
from fractions import Fraction
import time

EPS = 1e-08


def vol(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)


WHITE = 1
GRAY = 0
BLACK = -1


class Pt:
    id = 0

    def __init__(self, x, y, color=BLACK):
        self.x = Fraction(x)
        self.y = Fraction(y)
        self.color = color
        Pt.id = 1 + Pt.id
        return

    def mul(c, pt, col=BLACK):
        return Pt(c*pt.x, c*pt.y, color=col)

    def __repr__(self):
        return '(' + self.x.__str__() + ", " + self.y.__str__() + ')'

    def __eq__(self, p):
        if (type(p) != type(self)):
            return False
        return abs(self.x - p.x) + abs(self.y - p.y) <= EPS

    def __lt__(self, p):
        ''' less than in \"lexicographical\" order '''
        if (self.y > p.y):
            return True
        if (self.y == p.y):
            return self.x < p.x
        return False

    '''
    def __gt__(self, p):
        if (self.y < p.y):
            return True
        if (self.y == p.y):
            return self.x > p.x
        return False

    def __ge__(self, p):
        if (self.y < p.y):
            return True
        if (self.y == p.y):
            return self.x >= p.x
        return False'''

    def __hash__(self):
        return (self.x, self.y, self.color).__hash__()

    def cmpLexicographicaly(self, other):
        ''' less than in \"lexicographical\" order '''
        if (self.y > other.y):
            return True
        if (self.y == other.y):
            return self.x < other.x
        return False

    def cmpByDistance(self, other):
        return self.x**2 + self.y**2 < other.x**2 + other.y**2


class Edge:
    id = 0
    height = 0  # уровень заметающей прямой. Нужно для сравнения

    def __init__(self, leftPt, rightPt, isRay=False, color=GRAY):
        self.isRay = isRay
        if (leftPt < rightPt):
            self._left = leftPt
            self._right = rightPt
        else:
            self._left = rightPt
            self._right = leftPt
        #self._left.color = color
        #self._right.color = color
        self.id = Edge.id
        Edge.id += 1
        # self.height = 0
        return

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def containPt(self, p):
        ox = self.left.x
        oy = self.left.y
        ax = self.right.x
        ay = self.right.y
        bx = p.x
        by = p.y
        d = (bx - ox)*(ay - oy) - (ax - ox)*(by - oy)
        s = (bx - ox)*(ax - ox) + (ay - oy)*(by - oy)
        b1 = d == 0 and s >= 0
        c = s / ((ax - ox)**2 + (ay - oy)**2)
        return b1 and c**2 <= 1
        # xs = ((p.x - self.lefteft.x)**2 + (p.y - self.lefteft.y)**2)**0.5
        # ys = ((p.x - self.rightight.x)**2 + (p.y - self.rightight.y)**2)**0.5
        # s = ((self.lefteft.x - self.rightight.x)**2 +
        # (self.lefteft.y - self.rightight.y)**2)**0.5
        # abs(s**2 - xs**2 - ys**2 - 6*xs*ys - 2*(xs + ys)*(s - xs - ys)) < EPS
        # return abs(s - xs - ys) < EPS

    def _intersection(Ax, Ay, Bx, By):  # x координата пересечения с заметающей
        alpha = By - Edge.height
        beta = Edge.height - Ay
        return (alpha*Ax + beta*Bx) / (alpha + beta)
        # return (Bx*(Ay - Edge.height) + Ax*(Edge.height - By))/(Ay - By)

    def isIntersectLine(self, height=None):
        if (height is None):
            height = Edge.height
        return self.left.y >= height and height >= self.right.y

    def getIntersection_line(self):
        return Edge._intersection(self.left.x, self.left.y,
                                  self.right.x, self.right.y)

    def fromCoordinates(x1, y1, x2, y2, color=GRAY):
        return Edge(Pt(x1, y1, color=color), Pt(x2, y2, color=color))

    def __repr__(self):
        return '{left} - {right} Edge'.format(left=self.left, right=self.right)

    def __hash__(self):
        return hash((self.left.x, self.left.y, self.right.x, self.right.y))

    def isIntersect(self, edge):
        return vol(self.left, self.right, edge.left) * \
            vol(self.left, self.right, edge.right) <= 0 \
            and vol(edge.left, edge.right, self.left) * \
            vol(edge.left, edge.right, self.right) <= 0

    def getIntersection(self, edge):
        prod1 = vol(edge.left, edge.right, self.left)
        prod2 = vol(edge.left, edge.right, self.right)
        prod3 = vol(edge.left, self.left, self.right)
        color = GRAY  # пересечение общего вида
        try:
            resX = self.left.x + (self.right.x - self.left.x) * \
                abs(prod1)/abs(prod2-prod1)
            resY = self.left.y + (self.right.y - self.left.y) * \
                abs(prod1)/abs(prod2-prod1)
        except(ZeroDivisionError):
            resX = self.right.x
            resY = self.right.y
            color = BLACK
        if abs(prod1) < 10*EPS or abs(prod2) < 10*EPS or abs(prod3) < 10*EPS:
            color = BLACK  # точка пересечения совпала с вершиной
        res = Pt(resX, resY, color)
        print('returned intersection = {pt}, col={c}'.format(pt=res, c=color))
        return res

    def __lt__(self, edge):
        if (self.isIntersectLine() and edge.isIntersectLine()):
            # если оба отрезка пересекают заметающую прямую
            Ax = self.left.x
            Bx = self.right.x
            Cx = edge.left.x
            Dx = edge.right.x
            Ay = self.left.y
            By = self.right.y
            Cy = edge.left.y
            Dy = edge.right.y
            Ex = None
            Fx = None
            if (Ay != By):
                Ex = Edge._intersection(Ax, Ay, Bx, By)
            if (Cy != Dy):
                Fx = Edge._intersection(Cx, Cy, Dx, Dy)
            if (Ex is None):
                if (Fx is None):
                    return Ax < Cx
                return Ax < Fx
            else:
                if Fx is None:
                    return Ex < Cx
            return Ex < Fx  # Cx
        return Pt.cmpLexicographicaly(self.left, edge.left)
        # raise Exception('Один из отрезков не пересекает заметающую прямую')

    def __le__(self, edge):
        return self < edge or self == edge

    def __eq__(self, edge):
        return self.left == edge.left and self.right == edge.right


class Ray:
    def __init__(self, p):
        if p.x != 0:
            self.target = Pt(1, p.y/p.x)
        else:
            self.target = Pt(p.x/p.y, 1)
        # self.target = p

    def fromEdge(edge):
        pt = edge.left if edge.left != Pt(0, 0) else edge.right
        return Ray(pt)

    def isIntersect(self, edge):
        return vol(self.target, Pt(0, 0), edge.left) * \
               vol(self.target, Pt(0, 0), edge.r) <= 0
        #  для луча не подходит

    def getIntersection(self, edge):
        prod1 = vol(edge.l, edge.r, self.target)
        prod2 = vol(edge.l, edge.r, Pt(0, 0))
        if (prod2 == 0):
            raise Exception('prod2 == 0')
            pass
        resX = self.target.x + (0 - self.target.x)*abs(prod1)/abs(prod2-prod1)
        resY = self.target.y + (0 - self.target.y)*abs(prod1)/abs(prod2-prod1)
        return Pt(resX, resY)

    def containPt(self, pt):
        ax = self.target.x
        ay = self.target.y
        bx = pt.x
        by = pt.y
        d = bx*ay - ax*by
        s = bx*ax + ay*by
        b1 = d == 0 and s >= 0
        return b1

    def __eq__(self, other):
        return self.containPt(other.target) or other.containPt(self.target)

    def __hash__(self):
        return hash(self.target)

    def __repr__(self):
        return 'Ray' + self.target.__repr__()


intersections = dict()  # avl.Leaf()
q = dict()
pts = dict()    # ключ - луч из 0. Значения - точки на этом луче,
                # упорядоченные по расстоянию от 0
s = avl_b.LeafN()

tau = avl_b.LeafN()
vertices = avl_b.LeafN()

# ВХОДНЫЕ ДАННЫЕ
input_edges = [Edge.fromCoordinates(3.0, 1.0, 4.0, 0.0, color=BLACK),
               Edge.fromCoordinates(0.0, 4.0, 1.0, 3.0, color=BLACK),
               Edge.fromCoordinates(4.0, 1.0, 1.0, 4.0, color=BLACK),
               Edge.fromCoordinates(6.0, 5.0, 5.0, 6.0, color=BLACK),
               Edge.fromCoordinates(2.0, 0.0, 1.0, 2.0, color=BLACK)
               ]

for i in range(10, 12):
    input_edges.append(Edge.fromCoordinates(i + 1.0, 0.0,
                                            i + 1.0, 1.0, color=BLACK))
    # input_edges.append(Edge.fromCoordinates(i + 0.5, 20.0,
    #                                        i + 1.0, 20.0, color=BLACK))


edges = input_edges.copy()
rays = dict()

R = 1000.0

for e in edges:
    vertices = vertices.insert((e.left, e.right))
    s = s.insert(e.left)
    s = s.insert(e.right)

# добавляем отрезки из начала, попутно создаём лучи
for v in s:
    e = Edge(Pt(0.0, 0.0), Pt.mul(R, v), isRay=True)
    r = Ray.fromEdge(e)
    if (r not in pts):
        pts[r] = avl_b.LeafN()
        edges.append(e)
    rays[e] = avl_b.LeafN()


edges.sort(key=lambda x: x.left)  # n ln n
# print(edges)

for e in edges:
    if (q.get(e.left) is None):
        q[e.left] = avl_b.LeafN()
    if (q.get(e.right) is None):
        q[e.right] = avl_b.LeafN()
    q[e.left] = q[e.left].insert(e)
    s = s.insert(e.left)
    s = s.insert(e.right)


def HandleEvent(p):
    # p.color = BLACK
    intersections[p] = avl_b.LeafN()
    print('##################################################################')
    print('p = {pt}'.format(pt=p))
    global tau
    global q

    # выбрали высоту
    Edge.height = p.y
    print('Height = {ht}'.format(ht=Edge.height))
    ###########################################################
    # step 1
    U = avl_b.LeafN()
    if q.get(p) is not None:
        U = U.update(q[p])

    ###########################################################
    # step 2
    c = avl_b.LeafN()
    low = avl_b.LeafN()
    for e in tau:
        # по сложности не получается
        if (e.containPt(p)):
            if (e.right == p):
                low = low.insert(e)
            else:
                if (e.left != p):
                    c = c.insert(e)

    ###########################################################
    # steps 3, 4
    # unionP = U.update(c, low)
    print('UnuionUCL = ({un}, {cn}, {ln})'.format(
        un=len(U),
        cn=len(c),
        ln=len(low)))
    #  print(c)
    print('#####')
    if (len(U) + len(c) + len(low) > 1):
        intersections[p] = intersections[p].update(U, c, low)
    ###########################################################
    # step 5
    tau = tau.difference(low, c)
    ###########################################################
    # step 6
    Edge.height = p.y - 10*EPS  # теперь сравнение делается по другой высоте
    for e in U:
        try:
            tau = tau.insert(e)
        except(Exception):
            print('exc')
    for e in c:
        try:
            tau = tau.insert(e)
        except(Exception):
            print('exc')
    ###########################################################
    # step 8...
    uc = c.copy()
    for e in U:
        try:
            uc = uc.insert(e)
        except(Exception):
            print('exc at uc')
    # uc = c.update(U)
    # if e.isRay:
    #    rays[e] = rays[e].update(tau)
    # tau1 = tau  # avl.Leaf().update(tau)
    if len(uc) == 0:
        # print('low == {l1}'.format(l1=low))
        try:
            if len(low) > 1:
                print(p)
            s1 = tau.getPrev(low.findmin().key)
            s2 = tau.getNext(low.findmax().key)
            print('FNE1({s1}, {s2})'.format(s1=s1, s2=s2))
            findNewEvent(s1, s2, p)
        except(AttributeError, Exception):
            pass
    else:
        try:
            s1 = uc.findmin().key
            s2 = tau.getPrev(s1)
            print('FNE2({s1}, {s2})'.format(s1=s1, s2=s2))
            findNewEvent(s1, s2, p)
        except(AttributeError, IndexError, Exception):
            pass
        try:
            s1 = uc.findmax().key
            s2 = tau.copy().getNext(s1)
            print('FNE3({s1}, {s2})'.format(s1=s1, s2=s2))
            findNewEvent(s1, s2, p)
        except(AttributeError, IndexError, Exception):
            pass
    ###########################################################
    return


def findNewEvent(s1, s2, p):
    global intersections
    global s
    if s1.isRay and s2.isRay:
        return
    if s1.isIntersect(s2):
        print('    {s1} intersects {s2}'.format(s1=s1, s2=s2))
        i = s1.getIntersection(s2)
        if i > p:
            print('    new intersection {pt}'.format(pt=i))
            if intersections.get(i) is None:
                intersections[i] = avl_b.LeafN()
            intersections[i] = intersections[i].update([s1, s2])
            s = s.insert(i)
    return



start = time.time()
while len(s) > 0:
    v = s.findmin().key
    s = s.removemin()
    start1 = time.time()
    HandleEvent(v)
    end1 = time.time()
    # print('ELAPSED TIME: {t}'.format(t=end1 - start1))

end = time.time()

Pt.__lt__ = Pt.cmpByDistance  # сравниваем по расстоянию

for x in intersections:
    if x != Pt(0, 0, BLACK) and x != Pt(0, 0):
        r = Ray(x)
        if (r not in pts):
            pts[r] = avl_b.LeafN()
        pts[r] = pts[r].insert(x)

print('--------------------------------------------------')
print('Output:')
visible = set()
for ray in pts:
    print('ray target is {t}'.format(t=ray.target))
    nearestPt = pts[ray].findmin().key
    print('nearest Point is {pt}'.format(pt=nearestPt))
    # print(nearestPt, ':')
    print('nearest Point color is {col}'.format(col=nearestPt.color))
    if nearestPt.color == BLACK:
        # если ближайшая точка граничная, то смотрим следующую
        for e in intersections[nearestPt]:
            if not e.isRay:
                print('1. edge is {e}'.format(e=e))
                visible.add(e)
        nextPt = pts[ray].getNext(nearestPt)
        print('next pt is {pt} and has color {color}'.format(pt=nextPt,
              color=nextPt.color))
        if nextPt.color != BLACK:
            # если следующая точка не граничная
            for e in intersections[nextPt]:
                if not e.isRay:
                    print('2. edge is {e}'.format(e=e))
                    visible.add(e)
    else:
        #  иначе
        for e in intersections[nearestPt]:
            if not e.isRay:
                print('3. edge is {e}'.format(e=e))
                visible.add(e)

print('Visible edges are: {vis}'.format(vis=visible))
print('ELAPSED TIME: {t}. e = {l}, i = {i}'.format(
        t=end - start, 
        l=len(input_edges), 
        i=len(intersections)))
results.append((end - start, len(input_edges), len(intersections)))
