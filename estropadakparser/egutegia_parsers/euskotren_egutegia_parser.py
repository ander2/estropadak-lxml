import lxml.html
from ..estropada.estropada import Estropada


class EuskotrenEgutegiaParser():
    '''Base class to parse the Euskotren calendar'''

    def __init__(self):
        self.document = ''
        self.estropada = None

    def parse(self, content):
        document = lxml.html.fromstring(content)
        self.liga = 'euskotren'
        selector = '.tabla_2 tbody tr'
        estropadak = []
        table_rows = document.cssselect(selector)
        for row in table_rows:
            anchor = row.cssselect('a')
            izena = anchor[0].text.strip()
            link = "http://www.euskolabelliga.com" + anchor[0].attrib['href'].replace('calendario', 'resultados')
            lekua = row.cssselect('td')[2].text.strip()
            data = row.cssselect('td')[3].text.strip()
            ordua = row.cssselect('td')[4].text.strip().replace('.', ':')
            data_osoa = '%s %s' % (data, ordua)
            opts = { 'urla': link, 'lekua': lekua, 'data': data_osoa, 'liga': self.liga}
            estropada = Estropada(izena, **opts)
            estropadak.append(estropada)
        return estropadak