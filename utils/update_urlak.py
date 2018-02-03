'''
    Script to update url and lekua for estropadak in league and year
'''
import couchdb
import urllib.request
import logging
from estropadakparser.estropadakparser import ActEgutegiaParser, EstropadakParser

couch = couchdb.Server('http://admin:admin123@127.0.0.1:5984')
db = couch['estropadak']


def getEstropadakfromDB(urtea):
    league = 'ACT'
    fyear = "{}".format(urtea)
    fyearz = "{}".format(urtea + 1)

    start = [league, fyear]
    end = [league, fyearz]
    try:
        estropadak = db.view("estropadak/all",
                                None,
                                startkey=start,
                                endkey=end,
                                include_docs=False,
                                reduce=False)
        print(estropadak.total_rows)
    except couchdb.http.ResourceNotFound:
        return []
    return estropadak.rows

def parseEgutegia(urtea):
    url = 'http://www.euskolabelliga.com/resultados/index.php?id=eu&t={}'.format(urtea)
    file = urllib.request.urlopen(url)
    content = file.read()
    parser = ActEgutegiaParser()
    estropadak = parser.parse(content)
    return estropadak


for urtea in range(2010, 2011):
    print("{:=^40}".format(urtea))
    estropadak = parseEgutegia(urtea)
    estropadakDB = getEstropadakfromDB(urtea)
    estropadakByName = {estropada['key'][2]: estropada['id'] for estropada in estropadakDB}
    for estropada in estropadak:
        try:
            izena = estropada.izena
            ida = estropadakByName[estropada.izena]
            print("Match {} == {}".format(izena, ida))
            db_estropada = db[ida]
            db_estropada['urla'] = estropada.urla
            db_estropada['lekua'] = estropada.lekua
            doc_id, doc_rev = db.save(db_estropada)
            print("{} {}".format(doc_id, doc_rev))
        except KeyError as e:
            logging.error("No match for %s", e)
