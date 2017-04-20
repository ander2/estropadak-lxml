import lxml.html
import urllib
import couchdb
import json
import sys

couch = couchdb.Server('http://admin:admin123@127.0.0.1:5984')
db = couch['estropadak']

liga = str(sys.argv[1])
urtea = str(sys.argv[2])
print('{} {}'.format(liga, urtea))
estropadak = db.view('estropadak/all', None, startkey=[liga,urtea],endkey=[liga,urtea + "z"])
for estropada in estropadak:
    print(u"{} {}".format(estropada.key[1], estropada.key[2]))

