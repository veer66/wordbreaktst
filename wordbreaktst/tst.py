#
# Copyright (c) 2007 Vee Satayamas
# 
# This file is part of WordBreak TST.
# 
# KunyitTst is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# KunyitTst is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

class TstIter:
    def __init__(self, tst):
        self._tst = tst
        self._n = tst.get_dummy()
        self._valid = True
        
    def apply(self, ch):
        if not self._valid:
            return False
        if isinstance(ch, str) or isinstance(ch, unicode):
            ch = ord(ch)
        self._n = self._tst.goto_child(self._n)
        if self._n == None:
            return False
        self._n = self._tst.find_sibling(self._n, ch)
        self._valid = (self._n != None)
        return self._valid
        
    def is_break_pos(self):
        if not self._valid:
            return False
        return self._tst.is_break_pos(self._n)
        
    def get_value(self):
        return self._tst.get_value(self._n)
        
    def has_suffix(self):
        return self._tst.has_suffix_at(self._n)

class Tst:
    KEY   = 0
    VAL   = 1
    LEFT  = 2
    RIGHT = 3
    CHILD = 4
    IS_BREAK_POS = 5
    
    SIZE  = 6

    def __init__(self):
        self._nodes = []
        self._free = []
        self._n = 0
        self._dummy = self._new_node() 
        self._root = self._new_node()
        self.connect_dummy_and_root()
    
    def has_suffix_at(self, n):
        return (self._nodes[n * Tst.SIZE + Tst.CHILD] != None)
        
    def has_prefix(self, prefix):
        i = self.iterator()
        for ch in prefix:
            if not i.apply(ch):
                return False
        return i.has_suffix()

    def prefix_matches(self, prefix):
        i = self.iterator()
        for ch in prefix:
            if not i.apply(ch):
                return

        if self.is_break_pos(i._n):
            yield base, self._nodes[i._n * Tst.SIZE + Tst.VAL]

        for pair in self._subtree(prefix, self.goto_child(i._n)):
            yield pair

    def _subtree(self, base, n):
        if n is None:
            return

        here = n * Tst.SIZE
        prefix = base + unichr(self._nodes[here + Tst.KEY])

        if self.is_break_pos(n):
            yield prefix, self._nodes[here + Tst.VAL]

        for pair in self._subtree(prefix, self._nodes[here + Tst.CHILD]):
            yield pair
        for pair in self._subtree(base, self._nodes[here + Tst.LEFT]):
            yield pair
        for pair in self._subtree(base, self._nodes[here + Tst.RIGHT]):
            yield pair

    def connect_dummy_and_root(self):
        self._nodes[self._dummy * Tst.SIZE + Tst.CHILD] = self._root
  
    def get_dummy(self):
        return self._dummy
  
    def iterator(self):
        return TstIter(self)
  
    def has_key(self, k):
        i = self.iterator()
        for ch in k:
            if not i.apply(ch):
                return False
        return i.is_break_pos()
        
    def is_break_pos(self, n):
        return self._nodes[n * Tst.SIZE + Tst.IS_BREAK_POS]
        
    def get_value(self, n):
        return self._nodes[n * Tst.SIZE + Tst.VAL]
  
    def goto_child(self, n):
        return self._nodes[n * Tst.SIZE + Tst.CHILD]
        
    def find_sibling(self, n, k):
        while k != self._nodes[n * Tst.SIZE + Tst.KEY]:
            if k < self._nodes[n * Tst.SIZE + Tst.KEY]:
                if self._nodes[n * Tst.SIZE + Tst.LEFT] == None:
                    return None
                else:
                    n = self._nodes[n * Tst.SIZE + Tst.LEFT]
                #end if
            elif k > self._nodes[n * Tst.SIZE + Tst.KEY]:
                if self._nodes[n * Tst.SIZE + Tst.RIGHT] == None:
                    return None
                else:
                    n = self._nodes[n * Tst.SIZE + Tst.RIGHT]
                #end if
            #end if
        #end while 
        return n
                
  
    def get_root(self):
        return self._root
  
    def _new_node(self):
        if self._free:
            return self._free.pop()

        entry = [None] * Tst.SIZE
        entry[Tst.IS_BREAK_POS] = False
        self._nodes.extend(entry)
        self._n += 1
        return self._n - 1

    def insert(self, k, v):
        p = self._root * Tst.SIZE
        for i, ch in enumerate(k):            
            c = ord(ch)            
            while self._nodes[p + Tst.KEY] != c:
                if self._nodes[p + Tst.KEY] == None:
                    self._nodes[p + Tst.KEY] = c
                elif c < self._nodes[p + Tst.KEY]:
                    if self._nodes[p + Tst.LEFT] == None:
                        self._nodes[p + Tst.LEFT] = self._new_node()
                    p = self._nodes[p + Tst.LEFT] * Tst.SIZE
                elif c > self._nodes[p + Tst.KEY]:
                    if self._nodes[p + Tst.RIGHT] == None:
                        self._nodes[p + Tst.RIGHT] = self._new_node()
                    p = self._nodes[p + Tst.RIGHT] * Tst.SIZE
            #end while
            if i + 1 != len(k):
                if self._nodes[p + Tst.CHILD] == None:
                    self._nodes[p + Tst.CHILD] = self._new_node()
                p = self._nodes[p + Tst.CHILD] * Tst.SIZE
        #end for
        self._nodes[p + Tst.IS_BREAK_POS] = True
        self._nodes[p + Tst.VAL] = v                
                
    def insert_sorted_array(self, a):
        self._insert_sorted_array_rec(a, 0, len(a))

    def _insert_sorted_array_rec(self, a, l, r):
        if l < r:
            m = (l + r) / 2
            self.insert(a[m][0], a[m][1])
            self._insert_sorted_array_rec(a, l, m)
            self._insert_sorted_array_rec(a, m + 1, r)

    def remove(self, k):
        path = []
        i = self.iterator()
        for ch in k:
            if not i.apply(ch):
                raise IndexError("No such element in tree.")
            path.append(i._n)

        self._nodes[path[-1] * Tst.SIZE + Tst.IS_BREAK_POS] = False

        if self._nodes[path[-1] * Tst.SIZE + Tst.CHILD]:
            return

        prev = None
        for node in path[::-1]:
            n = node * Tst.SIZE
            if (self._nodes[n + Tst.LEFT] or self._nodes[n + Tst.RIGHT]):
                if self._nodes[n + Tst.CHILD] == prev:
                    self._nodes[n + Tst.CHILD] = None
                break
            prev = node
            self._nodes[n:n + Tst.SIZE] = [None] * Tst.SIZE
            self._nodes[n + Tst.IS_BREAK_POS] = False
            self._free.append(node)
