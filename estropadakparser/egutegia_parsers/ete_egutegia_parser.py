import datetime
import re
import lxml.html
from ..estropada.estropada import Estropada


class EteEgutegiaParser(object):
    '''Base class to parse the ETE calendar'''

    def __init__(self):
        self.document = ''
        self.estropada = None
        self.liga = 'ETE' 

    def parse_year(self):
        selector = 'h1 span span'
        h1_sections = self.document.cssselect(selector)
        year = datetime.datetime.now().year
        if len(h1_sections) > 0:
            year = int(h1_sections[0].text.strip())
        return year

    def parse_date(self, row):
        year = self.parse_year()
        data_html = row.cssselect('.fecha span')
        data_elements = data_html[0].text.strip().split()
        day = int(data_elements[0])
        month = data_elements[1]
        month_num = '06'
        if month == 'Julio':
            month_num = '07'
        elif month == 'Agosto':
            month_num = '08'
        elif month == 'Septiembre':
            month_num = '09'
        month_num = int(month_num)
        date = datetime.datetime(year=year, month=month_num, day=day)
        return date.isoformat()

    def parse(self, content):
        self.document = lxml.html.fromstring(content)
        selector = 'tr.tab-item.g1'
        estropadak = []
        table_rows = self.document.cssselect(selector)
        for row in table_rows:
            anchor = row.cssselect('a')
            izena = anchor[0].text.strip()
            link = anchor[0].attrib['href']
            data = self.parse_date(row)
            opts = { 
                'urla': link,
                'data': data,
                'liga': self.liga
            }
            estropada = Estropada(izena, **opts)
            estropadak.append(estropada)
        return estropadak
