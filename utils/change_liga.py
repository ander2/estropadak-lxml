import lxml.html
import urllib
import couchdb
import json
import sys

couch = couchdb.Server('http://admin:admin123@127.0.0.1:5984')
db = couch['estropadak']

urtea = str(sys.argv[1])
estropadak = db.view('estropadak/all', None, startkey=["Euskotren",urtea],endkey=["Euskotren",urtea + "z"])
for estropada in estropadak:
    print(u"{} {}".format(estropada.key[1], estropada.key[2]))
    # liga = raw_input('Liga:')
    # liga = liga.strip()
    liga_izena = 'euskotren'
    # if liga == "1" or liga == "2":
    #     print "MAtch"
    #     liga_izena = 'ARC' + liga
    # else:
    #     print "no Match"
    #     liga_izena = 'ARC1'
    estrop = db[estropada.id]
    estrop['liga'] = liga_izena
    db.save(estrop)
