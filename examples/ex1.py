import cPickle as pickle
from wordbreaktst import Tst

tst = Tst()
tst = pickle.load(open("wordlist.pickle"))
print tst.has_key(u"man")
print tst.has_key(u"ma")
print tst.has_key(u"foo")
