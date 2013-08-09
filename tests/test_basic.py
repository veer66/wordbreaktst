#
# Copyright (c) 2007 Vee Satayamas
# 
# This file is part of WordBreak Tst.
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

from wordbreaktst import Tst
class TestBasic(object):
    def setup(self):
        self.tst = Tst()

    # Now py.test can do its thing too:
    def setup_method(self, method):
        self.setup()

    def test_happy_insert(self):
        self.tst.insert(u"abc", 1)

    def test_happy_insert_gotochild(self):
        self.tst.insert(u"abc", 1)
        assert self.tst.goto_child(self.tst.get_root()) == 2
        assert self.tst.goto_child(2) == 3

    def test_get_value(self):
        self.tst.insert(u"abc", 1)
        self.tst.get_value(2) == 1
        
    def test_find_sibling(self):
        self.tst.insert(u"abc", 1)
        assert self.tst.find_sibling(1, ord(u"a")) == 1

    def test_get_root(self):
        assert self.tst.get_root() == 1

    def test_get_iterator(self):
        self.tst.insert(u"abc", 1)
        i = self.tst.iterator()
        assert i.apply(u"a") == True
        assert i.apply(u"b") == True
        assert i.apply(u"c") == True 
      
    def test_goto_child(self):
        assert self.tst.goto_child(self.tst.get_root()) == None
        
    def test_has_key_empty(self):
        assert self.tst.has_key("abc") == False

    def test_has_key_happy(self):
        self.tst.insert(u"abc", 1)
        assert self.tst.has_key("abc") == True

    def test_has_key_prefix(self):
        self.tst.insert(u"abc", 1)
        assert self.tst.has_key("ab") == False
        
    def test_has_key_prefix(self):
        self.tst.insert(u"abc", 1)
        assert self.tst.has_prefix(u"a") == True
        assert self.tst.has_prefix(u"ab") == True
        assert self.tst.has_prefix(u"abc") == False
        assert self.tst.has_prefix(u"x") == False
        
    def test_is_break_at_start_state(self):
        i = self.tst.iterator()
        assert i.is_break_pos() == False
    
    def test_is_break_at_false_state(self):
        i = self.tst.iterator()
        i.apply(u"k")
        assert i.is_break_pos() == False

    def test_remove_simple(self):
        self.tst.insert('foobar', 1)
        self.tst.remove('foobar')
        assert not self.tst.has_key('foobar')
        assert not self.tst.has_prefix('foobar')
        assert len(self.tst._free) == 6

    def test_remove_multiple(self):
        lmnts = set([u"foo", u"bar", u"baz", u"bard", u"bicker", "tomb"])
        for lmnt in lmnts:
            self.tst.insert(lmnt, 1)

        self.tst.remove(u"bicker")
        assert not self.tst.has_key(u"bicker")
        assert not self.tst.has_prefix(u"bi")
        assert len(self.tst._free) == 5 # reclaimed 'icker' tail

        for lmnt in lmnts - set([u"bicker"]):
            assert self.tst.has_key(lmnt)

        self.tst.remove(u"bar")
        assert not self.tst.has_key(u"bar")
        assert self.tst.has_prefix(u"bar")
        assert len(self.tst._free) == 5 # no 'tail' could be reclaimed

        for lmnt in lmnts - set([u"bicker", u"bar"]):
            assert self.tst.has_key(lmnt)

    def test_insert_remove_mix(self):
        self.tst.insert('foo', 1)
        self.tst.insert('foobar', 1)
        self.tst.remove('foo')
        assert not self.tst.has_key('foo')
        assert self.tst.has_key('foobar')
        self.tst.insert('foo', 1)
        assert self.tst.has_key('foo')

    def test_prefix_matches(self):
        for lmnt in [u"foo", u"bar", u"baz", u"baddie", u"bicker", "tomb"]:
            self.tst.insert(lmnt, 1)

        matches = list(self.tst.prefix_matches(u"ba"))
        assert set([key for key, val in matches]) == \
            set([u"baddie", u"bar", u"baz"])
        matches = list(self.tst.prefix_matches(u"noo"))
        assert not matches
