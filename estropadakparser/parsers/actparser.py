import datetime
import re
from .parser import Parser
from ..estropada.estropada import Estropada, TaldeEmaitza

class ActParser(Parser):
    '''Base class to parse an ACT race result'''

    def __init__(self):
        pass

    def parse(self, *args):
        '''Parse a result and return an estropada object'''
        urla = args[0]
        document = self.get_content(*args)
        (estropadaName, estropadaDate, lekua) = self.parse_headings(document)
        opts = {'urla': urla, 'lekua': lekua, 'data': estropadaDate, 'liga': 'ACT'}
        self.estropada = Estropada(estropadaName, **opts)
        self.parse_tandas(document)
        resume = self.parse_resume(document)
        return self.estropada

    def calculate_points_positions(self):
        self.estropada.sailkapena.sort(key = lambda x: datetime.datetime.strptime(x.denbora, '%M:%S,%f'))
        for index, taldea in enumerate(self.estropada.sailkapena):
            taldea.posizioa = index + 1
            taldea.puntuazioa = len(self.estropada.sailkapena) + 1 - taldea.posizioa

    def parse_headings(self, document):
        '''Parse table headings'''
        heading_three = document.cssselect('h3')
        data = ''
        if len(heading_three) > 0:
            name = heading_three[0].text.strip()
            estropada = name.split('(')[0].strip()
            quoted_text = re.findall('\(([^\)]+)', name)
            for t in quoted_text:
                try:
                    data = datetime.datetime.strptime(t, '%Y-%m-%d')
                except ValueError:
                    estropada = estropada + t
        heading_table = document.cssselect('table[summary="Regata Puntuable"] td')
        lekua = ''
        if heading_table:
            lekua = heading_table[1].text.strip()
            ordua = re.split('[.:]', heading_table[3].text.strip())
            data_ordua = data.replace(hour=int(ordua[0], 10), minute=int(ordua[1], 10))
            data_text = data_ordua.strftime('%Y-%m-%d %H:%M')
        else:
            data_text = data_ordua.strftime('%Y-%m-%d')
        return (estropada, data_text , lekua)

    def parse_tandas(self, document):
        '''Parse race's paces tables'''
        tandas = document.find_class('tabla_tanda')
        for num, text in enumerate(tandas):
            rows = text.findall('.//tbody//tr')
            for row in rows:
                data = [x.text for x in row.findall('.//td')]
                kalea = int(data[0])
                emaitza = TaldeEmaitza(talde_izena=data[1].strip(),
                                       kalea=kalea, ziabogak=data[2:5],
                                       denbora=data[5], tanda=num + 1,
                                       tanda_postua=data[6], posizioa=0)
                self.estropada.taldeak_add(emaitza)

    def parse_resume(self, document):
        '''Parse race's resume table'''
        rank_table = '//table[@summary="Estropadaren sailkapena"]'
        try:
            sailkapena = document.xpath(rank_table)
            rows = sailkapena[-1].findall('.//tbody//tr')
        except:
            rows = []
        for num, row in enumerate(rows):
            try:
                if num == 0:
                    posizioa = row.find('.//td[1]//span').text.strip()
                else:
                    posizioa = row.find('.//td[1]').text.strip()
                team = row.find('.//td[2]').text.strip()
                puntuak = row.find('.//td[7]').text.strip()
                for i, taldea in enumerate(self.estropada.sailkapena):
                    if taldea.talde_izena == team:
                        try:
                            self.estropada.sailkapena[i].posizioa = int(posizioa, 10)
                            self.estropada.sailkapena[i].puntuazioa = int(puntuak, 10)
                        except:
                            print(f'Ez dago posizio edo puntuazioarik {team} taldearentzat')
            except:
                return None
