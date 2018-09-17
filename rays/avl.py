# -*- coding: utf-8 -*-
"""
Created on Tue May 29 17:05:58 2018

@author: ernst
"""

def stdcmp(a, b):
    return a < b


class Tree:
    def __init__(self, kvs=None, cmp=stdcmp):
        self.node = Leaf(cmp=stdcmp)
        return Leaf(cmp=stdcmp)

    def __setitem__(self, key, value):
        return

 # класс, описывающий узел дерева
class Node:
    def __init__(self, key, value=None, cmp=stdcmp):
        ''' cmp(a,b) - аналог a < b для ключей'''
        self._key = key
        self._val = value
        self._height = 1
        self._left = Leaf()
        self._right = Leaf()
        self._iter = self
        self.cmp = cmp
        return

    @property
    def key(self):
        return self._key

    def __len__(self):
        return 1 + len(self._left) + len(self._right)

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
        c = Node(self.key, self._val, cmp=self.cmp)
        c._left = self._left.copy()
        c._right = self._right.copy()
        return c

    def is_empty(self):
        return len(self) == 0

    def height(self):
        self._height = self.fixheight()
        return self._height

    def bfactor(self):
        return self._right.height() - self._left.height()

    def fixheight(self):
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
        return "({left} {key}[{val}] {right})".format(
                left=self._left,
                key=self.key,
                right=self._right,
                val=self._val if self._val is not None else '')

    def findmin(self):
        if (isinstance(self._left, Leaf)):
            return self
        return self._left.findmin()

    def findmax(self):
        if (isinstance(self._right, Leaf)):
            return self
        return self._right.findmax()

    def get(self, key, default=None):
        return self[key]
        # return default

    def _getPrev(self, key):
        if self.cmp(self.key, key):  # or self.key == key:
            if isinstance(self._right, Leaf):
                return self.key
            if self.cmp(self._right.key, key):
                return self._right.getPrev(key)
            return max(self.key, self._right.getPrev(key))
        if self.cmp(key, self.key) or self.key == key:
            if self._left.is_empty():
                return None
                # return self.key
            return self._left.getPrev(key)

    '''def getPr(self, cond):
        if cond(self.key):
            return self._left.getPr(cond)
        if isinstance(self._right, Leaf):
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
            return self._left.copy()  # .findmax().key
        if self.cmp(self.key, key):
            res = self.copy()
            res._right = res._right._getLT(key)
            return res.balance()
        res = self._left.copy()._getLT(key)
        return res.balance()

    def _getLT_unbalanced(self, key):
        if key == self.key:
            return self._left  # .findmax().key
        if self.cmp(self.key, key):
            self._right = self._right._getLT(key)
            return self
        res = self._left._getLT(key)
        return res

    def _getLT(self, key):
        if key == self.key:
            return self._left  # .findmax().key
        if self.cmp(self.key, key):
            self._right = self._right._getLT(key)
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
        if key == self.key:
            return self._right
        if self.cmp(key, self.key):
            self._left = self._left._getGT(key)
            return self.balance()
        res = self._right._getGT(key)
        return res.balance()

    def removemin(self):
        if (isinstance(self._left, Leaf)):
            return self._right
        self._left = self._left.removemin()
        return self.balance()

    def remove(self, key):
        if self.cmp(key, self._key):            
            self._left = self._left.remove(key)
        else:
            if self.cmp(self.key, key):
                self._right = self._right.remove(key)
            else:
                # key == self.key
                q = self._left
                r = self._right
                if (isinstance(r, Leaf)):
                    return q
                minimum = r.findmin()
                minimum._right = r.removemin()
                minimum._left = q
                return minimum.balance()
        return self.balance()

    def __iter__(self):
        self._iter = self.copy()
        return self

    def __next__(self, default=None):
        if (isinstance(self._iter, Leaf)):
            raise StopIteration()
        m = self._iter.findmin().key
        self._iter = self._iter.removemin()
        return m


 # класс, описывающий лист дерева
class Leaf(Node):
    def __init__(self, cmp=stdcmp):
        self.cmp = cmp
        return

    def __repr__(self):
        return ' '

    def __getitem__(self, key):
        return self
        raise IndexError()

    def __setitem__(self, key, value):
        return Node(key, value=value, cmp=self.cmp)

    def fixheight(self):
        return 0

    def bfactor(self):
        return 0

    def get(self, key, default=None):
        return default

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

    def copy(self):
        return Leaf()

    def height(self):
        return 0

    def __eq__(self, other):
        return isinstance(other, Leaf)

    def is_empty(self):
        return True

    def insert(self, key, value=None):
        return Node(
            key,
            value)

    def __next__(self):
        raise StopIteration()

    def is_member(self, value=None):
        return False

    def findmin(self):
        return None

    def findmax(self):
        return None

    def removemin(self):
        return self

    def remove(self, key):
        return self

    @property
    def left(self):
        return Leaf()

    @property
    def right(self):
        return Leaf()

    def __len__(self):
        return 0


# x = Leaf().update(range(10))
# y = x.copy()
