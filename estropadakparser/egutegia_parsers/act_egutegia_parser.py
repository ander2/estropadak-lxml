import lxml.html
from estropadakparser.estropada.estropada import Estropada


class ActEgutegiaParser(object):
    '''Base class to parse the ACT calendar'''

    def __init__(self):
        self.document = ''
        self.estropada = None
        self.base_url = 'http://www.euskolabelliga.com'
        self.liga = 'ACT'

    def parse(self, content):
        self.document = lxml.html.fromstring(content)
        table_rows = self.document.cssselect('.taula.tablepadding tr')
        estropadak = []
        for i, row in enumerate(table_rows):
            if i == 0:
                continue
            anchor = row.cssselect('.race_name a')
            izena = anchor[0].text.strip()
            link = anchor[0].attrib['href']
            lek_data = row.cssselect('.place')
            lekua = lek_data[0].text.strip()
            data = lek_data[1].text.strip()
            urla = self.base_url + link
            opts = {'urla': urla, 'data': data, 'lekua': lekua, 'liga': self.liga, 'sailkapena': []}
            estropada = Estropada(izena, **opts)
            estropadak.append(estropada)
        return estropadak
