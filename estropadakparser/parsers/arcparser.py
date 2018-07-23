import datetime
import re
from .parser import Parser
from ..estropada.estropada import Estropada, TaldeEmaitza


class ArcParser(Parser):
    '''Base class to parse an ARC race result'''

    def __init__(self):
        pass

    def parse(self, *args):
        '''Parse a result and return an estropada object'''
        urla = args[0]
        document = self.get_content(*args)
        (estropadaName, estropadaDate, lekua, liga) = self.parse_headings(document)
        opts = {'urla': urla, 'data': estropadaDate, 'liga': liga, 'lekua': lekua}
        self.estropada = Estropada(estropadaName, **opts)
        self.parse_tandas(document)
        self.parse_resume(document)
        return self.estropada

    def parse_headings(self, document):
        '''Parse headings table'''
        liga_selector = document.cssselect('h1.seccion span span')[0].text.lower()
        if 'grupo 1' in liga_selector:
            liga_taldea = 'ARC1'
        else:
            liga_taldea = 'ARC2'
        heading_two = document.cssselect('.resultado h2')
        estropada = heading_two[0].text.strip()
        date_block = document.cssselect('li.fecha')
        hour_block = document.cssselect('li.hora')
        resume_block = document.cssselect('.articulo ul li')
        # Remove map span
        lekua = ''
        if len(resume_block) == 4:
            resume_block[3].cssselect('span')[0].drop_tree()
            lekua = resume_block[3].text_content().strip()
        date = date_block[0].text_content().strip(" \n").replace('Fecha', '').strip(" \n")
        new_date = self.parse_date(date)
        hour = hour_block[0].text_content().replace('Hora', '').strip()
        race_date = new_date + " " + hour
        return (estropada, race_date, lekua, liga_taldea)

    def parse_date(self, date):
        new_date = date.replace('Jun', '06')
        new_date = new_date.replace('Jul', '07')
        new_date = new_date.replace('Ago', '08')
        new_date = new_date.replace('Sept', '09')
        date_list = re.split(' ', new_date)
        (day, month, year) = date_list
        if int(day) < 10:
            day = '0' + day
        new_date = year + "-" + month + "-" + day
        return new_date

    def parse_tandas(self, document):
        tandas = document.cssselect('table.tanda')
        for num, text in enumerate(tandas):
            rows = text.findall('.//tbody//tr')
            for kalea, row in enumerate(rows):
                data = [x.text for x in row.findall('.//td')]
                taldea = row.find('.//span//a')
                emaitza = TaldeEmaitza(talde_izena=taldea.text.strip(),
                                       kalea=kalea + 1, ziabogak=data[1:4],
                                       denbora=data[4], tanda=num + 1)
                self.estropada.taldeak_add(emaitza)

    def parse_resume(self, document):
        sailkapena = document.find_class('clasificacion-regata')
        if len(sailkapena) > 0:
            rows = sailkapena[0].findall('.//tbody//tr')
            tanda_posizioak = [0] + [1] * 7
            for pos, row in enumerate(rows):
                taldea = row.find('.//span//a').text.strip()
                try:
                    puntuak = row.find('.//td[3]').text.strip()
                except:
                    puntuak = 0
                for t in self.estropada.sailkapena:
                    if t.talde_izena == taldea:
                        try:
                            t.posizioa = pos + 1
                            t.tanda_postua = tanda_posizioak[t.tanda]
                            t.puntuazioa = int(puntuak)
                        except:
                            t.posizioa = 1
                            t.tanda_postua = tanda_posizioak[t.tanda]
                            t.puntuazioa = 0
                        tanda_posizioak[t.tanda] = tanda_posizioak[t.tanda] + 1

