import lxml.html
import urllib
import couchdb
import json
import sys

couch = couchdb.Server('http://admin:admin123@127.0.0.1:5984')
source = 'http://admin:admin123@127.0.0.1:5984/estropadak'
dest = 'http://admin:HHZ60Et4wxJLhLs@estropadak.net:5984/estropadak'
couch.replicate(source, dest)
