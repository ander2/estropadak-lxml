import datetime
import re
import lxml.html
from ..estropada.estropada import Estropada


class ArcEgutegiaParser(object):
    '''Base class to parse the ARC1/ARC2 calendar'''

    def __init__(self, liga):
        self.document = ''
        self.estropada = None
        self.liga = liga

    def parse_year(self):
        selector = 'h1 span span'
        h1_sections = self.document.cssselect(selector)
        year = datetime.datetime.now().year
        if len(h1_sections) > 0:
            year = int(h1_sections[0].text.strip())
        return year

    def parse_date(self, date):
        year = self.parse_year()
        new_date = date.replace('Junio', '06')
        new_date = new_date.replace('Julio', '07')
        new_date = new_date.replace('Agosto', '08')
        new_date = new_date.replace('Septiembre', '09')
        date_list = re.split(' ', new_date)
        day = int(date_list[0])
        month = int(date_list[1])
        date = datetime.datetime(year=year, month=month, day=day)
        return date.isoformat()

    def parse(self, content):
        self.document = lxml.html.fromstring(content)
        if self.liga == 'ARC1':
            selector = 'tr.tab-item.g1'
        else:
            selector = 'tr.tab-item.g2'
        estropadak = []
        table_rows = self.document.cssselect(selector)
        for row in table_rows:
            anchor = row.cssselect('a')
            izena = anchor[0].text.strip()
            link = anchor[0].attrib['href']
            lek_data = row.cssselect('.fecha span')
            data = self.parse_date(lek_data[0].text.strip())
            opts = {
                'urla': link,
                'data': data,
                'liga': self.liga
            }
            estropada = Estropada(izena, **opts)
            estropadak.append(estropada)
        return estropadak
