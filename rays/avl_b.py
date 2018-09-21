# -*- coding: utf-8 -*-
"""
Created on Tue May 29 17:05:58 2018

@author: ernst
"""

from classes import Edge, Pt, BLACK, Ray, EPS

def stdcmp(a, b):
    return a < b


class NodeE:  # класс, описывающий узел дерева
    def __init__(self, key, value=None, cmp=stdcmp):
        ''' cmp(a,b) - аналог a < b для ключей'''
        self._key = key
        self._val = value
        self._height = 1
        self._left = LeafN()
        self._right = LeafN()
        self._iter = self
        self.cmp = cmp
        return

    @property
    def key(self):
        return self._key

    def __len__(self):
        # считаем только листья
        return len(self._left) + len(self._right)

    def __eq__(self, other):
        return self.key == other.key and self._val == other._val and \
            self._right == other._right and self._left == other._left

    def __getitem__(self, key):
        if self.key == key:
            return self._val
        if self.cmp(self.key, key):
            return self._right[key]
        return self._left[key]

    def __setitem__(self, key, value):
        if self.key == key:
            self._val = value
            return
        if self.cmp(self.key, key):
            self._right[key] = value
            return
        self._left[key] = value

    def copy(self):
        c = NodeE(self.key, self._val, cmp=self.cmp)
        c._left = self._left.copy()
        c._right = self._right.copy()
        return c

    def is_empty(self):
        return len(self) == 0

    def areKeysCorrect(self):
        b = self.key == self._left.findmax().key
        return b and self._left.areKeysCorrect() and self._right.areKeysCorrect()

    def height(self):
        self._key = self._left.findmax()._key
        self._height = self.fixheight()
        return self._height

    def bfactor(self):
        return self._right.height() - self._left.height()

    def fixheight(self):
        # if self._key != self._left.findmax()._key:
        #    raise(Exception)
        hl = self._left.height()
        hr = self._right.height()
        return 1 + max(hl, hr)

    def _rotateRight(self):
        q = self._left
        self._left = q._right
        q._right = self
        self.fixheight()
        q.fixheight()
        return q

    def _rotateLeft(self):
        p = self._right
        self._right = p._left
        p._left = self
        self.fixheight()
        p.fixheight()
        return p

    def balance(self):
        self.fixheight()
        if (self.bfactor() >= 2):
            if self._right.bfactor() < 0:
                self._right = self._right._rotateRight()
            return self._rotateLeft()
        if self.bfactor() <= -2:
            if (self._left.bfactor() > 0):
                self._left = self._left._rotateLeft()
            return self._rotateRight()
        return self

    def insert(self, key, value=None):
        if key == self.key:
            self._val = value
            return self.balance()
        if self.cmp(key, self.key):
            self._left = self._left.insert(key, value)
        else:
            self._right = self._right.insert(key, value)
        return self.balance()

    def update(self, *iters):
        for it in iters:
            for e in it:
                self = self.insert(e)
        return self

    def difference(self, *iters):
        for it in iters:
            for e in it:
                self = self.remove(e)
        return self

    def __repr__(self):
        return "({left} [{val}] {right})".format(
                left=self._left,
                key=self.key,
                right=self._right,
                val=self._val if self._val is not None else '')

    def findmin(self):
        # Сложность: O(heigth)
        if (isinstance(self._left, LeafE)):
            return self
        return self._left.findmin()

    def findmax(self):
        # Сложность: O(heigth)
        if (isinstance(self._right, LeafE)):
            return self._right
        return self._right.findmax()

    def get(self, key, default=None):
        return self[key]
        # return default

    def _getPrev(self, key):
        if self.cmp(self.key, key):  # or self.key == key:
            if isinstance(self._right, LeafE):
                return self.key
            if self.cmp(self._right.key, key):
                return self._right._getPrev(key)
            return max(self.key, self._right._getPrev(key))
        if self.key == key:
            return self._left._getPrev(key)
        if self.cmp(key, self.key) or self.key == key:
            if self._left.is_empty():
                return None
                # return self.key
            return self._left._getPrev(key)

    '''def getPr(self, cond):
        if cond(self.key):
            return self._left.getPr(cond)
        if isinstance(self._right, LeafE):
            return self.key
        if cond(self._right.key):
            return self.key
        return self._right.getPr(cond)'''

    def getPrev(self, key):
        return self.getLessThan(key).findmax().key

    # def getPrev2(self, key):

        '''
        if self.key == key:
            return self.findmax().key
        if self.cmp(self.key, key):
            # s.key < key
            return _prevLoop(self.left, key, True)
        # s.key > key
        return _prevLoop(self.right, key, False)

    def _prevLoop(tree, key, state):
        b = tree.cmp(tree.key, key)
        if state and b:
            '''

    def getPrevFast(self, key):
        return self.getLessThan_unbalanced(key).findmax().key

    def getNext(self, key):
        return self.getGreaterThan(key).findmin().key

    def getLessThan_unbalanced(self, key):
        ''' returns a copy of the \'subtree\' whose keys are less
        than given key '''
        if key == self.key:
            return self._left.copy()  # .findmax().key
        if self.cmp(self.key, key):
            res = self.copy()
            res._right = res._right._getLT_unbalanced(key)
            return res
        res = self._left.copy()._getLT_unbalanced(key)
        return res

    def getLessThan(self, key):
        ''' returns a copy of the \'subtree\' whose keys
        are less than given key '''
        if key == self.key:
            return self._left.copy()._getLT(key)
        if self.cmp(self.key, key):
            res = self.copy()
            newR = res._right._getLT(key)
            if isinstance(newR, LeafN):
                res = res._left
            else:
                res._right = newR
            return res.balance()
        res = self._left.copy()._getLT(key)
        return res.balance()

    def _getLT_unbalanced(self, key):
        if key == self.key:
            return self._left
        if self.cmp(self.key, key):
            self._right = self._right._getLT(key)
            return self
        res = self._left._getLT(key)
        return res

    def _getLT(self, key):
        if key == self.key:
            return self._left._getLT(key)
        if self.cmp(self.key, key):
            newR = self._right._getLT(key)
            if isinstance(newR, LeafN):
                self = self._left
            else:
                self._right = newR
            return self.balance()
        res = self._left._getLT(key)
        return res.balance()

    def getGreaterThan(self, key):
        ''' returns a copy of the \'subtree\' whose keys are less than
        given key '''
        if key == self.key:
            return self._right.copy()
        if self.cmp(key, self.key):
            res = self.copy()
            res._left = res._left._getGT(key)
            return res.balance()
        res = self._right.copy()._getGT(key)
        return res.balance()

    def _getGT(self, key):
        # Сложность ln n
        if key == self.key:
            return self._right
        if self.cmp(key, self.key):
            self._left = self._left._getGT(key)
            return self.balance()
        res = self._right._getGT(key)
        return res.balance()

    def removemin(self):
        if (isinstance(self._left, LeafE)):
            return self._right
        self._left = self._left.removemin()
        return self.balance()

    def remove(self, key):
        if key == self.key:
            '''print(self)
            print('key = {key}, s.key = {skey}'.format(
                    key=key,
                    skey=self.key))'''
            # self._key = self._left.findmax().key
            if isinstance(self._left, LeafE):
                self = self._right
            else:
                self._left = self._left.remove(key)
                self._key = self._left.findmax().key  # TODO: убрать
            return self.balance()

        if self.cmp(key, self.key):
            if isinstance(self._left, LeafE):
                self = self._right
            else:
                self._left = self._left.remove(key)
        else:
            if self.cmp(self.key, key):
                if isinstance(self._right, LeafE):
                    if self._right.key == key:
                        self = self._left
                else:
                    self._right = self._right.remove(key)
            else:
                # отрезки пересеклись на высоте
                # этого не должно происходить при должном выборе высоты
                if key.isIntersectLine():
                    raise Exception('СП. sk={sk} k={k}'.format(sk=self.key, k=key))
                else:
                    raise Exception('СН. sk={sk} k={k} self={self}'.format(self=self, sk=self.key, k=key))
                h = Edge.height
                Edge.height = key.right.y
                self = self.remove(key)
                Edge.height = h
                print('key = {key}, s.key = {skey}'.format(
                        key=key,
                        skey=self.key))
                print(self)
                
        return self.balance()

    def __iter__(self):
        self._iter = self.copy()
        return self

    def __next__(self, default=None):
        if (isinstance(self._iter, LeafN)):
            raise StopIteration()
        m = self._iter.findmin().key
        self._iter = self._iter.removemin()
        return m


class LeafN(NodeE):  # класс, описывающий пустое дерево
    def __init__(self, cmp=stdcmp):
        self.cmp = cmp
        return

    def copy(self):
        return LeafN()

    def __repr__(self):
        return 'Empty tree'

    def findmax(self):
        raise AttributeError

    def __getitem__(self, key):
        raise IndexError()

    def getLessThan(self, key):
        return self

    def getLessThan_unbalanced(self, key):
        return self

    def _getLT(self, key):
        return self

    def _getLT_unbalanced(self, key):
        return self

    def getGreaterThan(self, key):
        return self

    def _getGT(self, key):
        return self

    def fixheight(self):
        return 0

    def balance(self):
        return self

    def __setitem__(self, key, value):
        return LeafE(key, value=value, cmp=self.cmp)

    def __eq__(self, other):
        return isinstance(other, LeafN)

    def is_empty(self):
        return True

    def insert(self, key, value=None):
        return LeafE(key, value=value, cmp=self.cmp)

    def __next__(self):
        raise StopIteration()

    def is_member(self, value=None):
        return False

    def areKeysCorrect(self):
        return True

    def __len__(self):
        return 0


class LeafE(NodeE):  # класс, описывающий лист дерева
    def __init__(self, key, value=None, cmp=stdcmp):
        self.cmp = cmp
        self._key = key
        self._val = value
        return

    def __repr__(self):
        return repr(self.key)

    @property
    def key(self):
        return self._key

    '''
    def __getitem__(self, key):
        return self
        raise IndexError()

    def __setitem__(self, key, value):
        return NodeE(key, value=value, cmp=self.cmp)
        '''

    def fixheight(self):
        return 1

    def bfactor(self):
        return 0

    def get(self, key, default=None):
        return default

    def getLessThan(self, key):
        if self.cmp(self.key, key):
            return self
        return LeafN()

    def getLessThan_unbalanced(self, key):
        return self.getLessThan(key)

    def _getLT(self, key):
        if self.cmp(self.key, key):
            return self
        return LeafN()

    def _getLT_unbalanced(self, key):
        return self.getLessThan(key)

    def getGreaterThan(self, key):
        if self.cmp(key, self.key):
            return self
        return LeafN()

    def _getGT(self, key):
        return self.getGreaterThan(key)

    def copy(self):
        return LeafE(self.key, value=self._val, cmp=self.cmp)

    def height(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, LeafE) and other.key == self.key \
            and self._val == other._val

    def is_empty(self):
        return False

    def insert(self, key, value=None):
        if self.key == key:
            self._val = value
            return self
        l, r = self.key, key
        if self.cmp(key, self.key):
            l, r = r, l
        res = NodeE(l, cmp=self.cmp)
        res._left = LeafE(l, cmp=self.cmp)
        res._right = LeafE(r, cmp=self.cmp)
        return res

    def __iter__(self):
        self._iter = True
        return self

    def __next__(self):
        if self._iter:
            self._iter = False
            return self.key
        raise StopIteration()

    def is_member(self, value=None):
        raise Exception('is_member unimplemented!')
        return value == self.key

    def findmin(self):
        return self

    def findmax(self):
        return self

    def removemin(self):
        return LeafN()

    def remove(self, key):
        if (self.key == key):
            return LeafN()
        return self

    def areKeysCorrect(self):
        return True

    '''
    @property
    def left(self):
        return LeafN()

    @property
    def right(self):
        return LeafN()
        '''

    def __len__(self):
        return 1


x = LeafN().update(range(10))
# y = x.copy()
