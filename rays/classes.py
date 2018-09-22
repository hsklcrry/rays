# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 13:04:38 2018

@author: IV_Ernst
"""

from fractions import Fraction

EPS = Fraction( 1e-08)


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
    event = None  # текущее событие
    isInserting = False  # Устанавливается в True перед вставкой рёбер и
    # в False перед удалением. Нужно для корректного сравнения рёбер из C

    def __init__(self, leftPt, rightPt, isRay=False):
        self.isRay = isRay
        if (leftPt < rightPt):
            self._left = leftPt
            self._right = rightPt
        else:
            self._left = rightPt
            self._right = leftPt
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
        return b1 and c <= 1
        # xs = ((p.x - self.lefteft.x)**2 + (p.y - self.lefteft.y)**2)**0.5
        # ys = ((p.x - self.rightight.x)**2 + (p.y - self.rightight.y)**2)**0.5
        # s = ((self.lefteft.x - self.rightight.x)**2 +
        # (self.lefteft.y - self.rightight.y)**2)**0.5
        # abs(s**2 - xs**2 - ys**2 - 6*xs*ys - 2*(xs + ys)*(s - xs - ys)) < EPS
        # return abs(s - xs - ys) < EPS

    def _intersection(Ax, Ay, Bx, By):  # x координата пересечения с заметающей
        return ((By - Edge.height)*Ax + (Edge.height - Ay)*Bx) / (By - Ay)
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
        prod4 = vol(edge.right, self.left, self.right)
        color = BLACK  # пересечение с вершиной
        try:
            resX = self.left.x + (self.right.x - self.left.x) * \
                abs(prod1)/abs(prod2-prod1)
            resY = self.left.y + (self.right.y - self.left.y) * \
                abs(prod1)/abs(prod2-prod1)
        except(ZeroDivisionError):
            resX = self.right.x
            resY = self.right.y
        if not(abs(prod1) < 10*EPS or
               abs(prod2) < 10*EPS or
               abs(prod3) < 10*EPS or
               abs(prod4) < 10*EPS):
            color = GRAY  # точка общего вида
        res = Pt(resX, resY, color)
        print('returned intersection = {pt}, col={c}'.format(pt=res, c=color))
        return res

    def isU(self):
        return self.left == Edge.event

    def isC(self):
        return self.left < Edge.event and Edge.event < self.right

    def isL(self):
        return self.right == Edge.event

    def __lt__(self, edge):
        if (self.isIntersectLine() and edge.isIntersectLine()):
            # если оба ребра пересекают заметающую прямую
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
            if Ex == Fx:
                if self.isU() and edge.isL():
                    return False
                if self.isL() and edge.isU():
                    return True
                if self.isU() and edge.isC() or self.isC() and edge.isU():
                    oldH = Edge.height
                    Edge.height = max(self.right.y, edge.right.y)
                    Ex = Edge._intersection(Ax, Ay, Bx, By)
                    Fx = Edge._intersection(Cx, Cy, Dx, Dy)
                    Edge.height = oldH
                    return Ex < Fx
                if self.isL() and edge.isC() or self.isC() and edge.isL():
                    oldH = Edge.height
                    Edge.height = min(self.left.y, edge.left.y)
                    Ex = Edge._intersection(Ax, Ay, Bx, By)
                    Fx = Edge._intersection(Cx, Cy, Dx, Dy)
                    Edge.height = oldH
                    return Ex < Fx
                if self.isU() and edge.isU():
                    oldH = Edge.height
                    Edge.height = max(self.right.y, edge.right.y)
                    Ex = Edge._intersection(Ax, Ay, Bx, By)
                    Fx = Edge._intersection(Cx, Cy, Dx, Dy)
                    Edge.height = oldH
                    return Ex < Fx
                if self.isL() and edge.isL():
                    oldH = Edge.height
                    Edge.height = min(self.left.y, edge.left.y)
                    Ex = Edge._intersection(Ax, Ay, Bx, By)
                    Fx = Edge._intersection(Cx, Cy, Dx, Dy)
                    Edge.height = oldH
                    return Ex < Fx
                if self.isC() and edge.isC():
                    oldH = Edge.height
                    if Edge.isInserting:
                        Edge.height = max(self.right.y, edge.right.y)
                    else:
                        Edge.height = min(self.left.y, edge.left.y)
                    Ex = Edge._intersection(Ax, Ay, Bx, By)
                    Fx = Edge._intersection(Cx, Cy, Dx, Dy)
                    Edge.height = oldH
                    return Ex < Fx
                print(self)
                print(self.isU())
                print(self.isC())
                print(edge)
                print(edge.isU())
                print(edge.isC())
                raise Exception
            return Ex < Fx  # Cx
        # return Pt.cmpLexicographicaly(self.left, edge.left)
        print('e1 = {e1}, e2 = {e2}'.format(e1=self, e2=edge))
        raise Exception('Один из отрезков не пересекает заметающую прямую')

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
