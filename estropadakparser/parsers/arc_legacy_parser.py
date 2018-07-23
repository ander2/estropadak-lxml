import datetime
import logging
import re
from .parser import Parser
from ..estropada.estropada import Estropada, TaldeEmaitza


class ArcParserLegacy(Parser):
    '''Base class to parse an ARC legacy(2006-2008) race result'''

    def __init__(self, **kwargs):
        pass

    def parse(self, *args):
        '''Parse a result and return an estropada object'''
        document = self.get_content(*args)
        urla = args[0]
        estropadaDate = args[2]
        liga = args[3]
        d = datetime.datetime.strptime(estropadaDate, '%Y-%m-%d')
        (estropadaName) = self.parse_headings(document)
        opts = {'urla': urla, 'data': estropadaDate, 'liga': liga}
        self.estropada = Estropada(estropadaName, **opts)
        self.parse_tandas(document, d.year)
        if d.year <= 2008:
            self.calculate_tanda_posizioa()
        else:
            self.parse_resume(document)
        return self.estropada

    def parse_headings(self, document):
        '''Parse headings table'''
        heading_one = document.cssselect('#contenido h1')
        estropada = heading_one[0].text.strip()
        estropada = estropada.replace("Resultados de: ", "")
        return (estropada)

    def parse_date(self, date):
        new_date = date.replace('Jun', '06')
        new_date = new_date.replace('Jul', '07')
        new_date = new_date.replace('Ago', '08')
        new_date = new_date.replace('Sept', '09')
        date_list = re.split('-', new_date)
        if len(date_list) == 3:
            new_date = date_list[2] + "-" + date_list[1] + "-" + date_list[0]
        return new_date

    def parse_tandas(self, document, urtea):
        tandas = document.cssselect('table.resultados')
        for num, text in enumerate(tandas):
            rows = text.findall('.//tr')
            for kalea, row in enumerate(rows):
                if kalea == 0:
                    continue
                data = [x.text for x in row.findall('.//td')]
                try:
                    if not data[1] is None:
                        if urtea < 2008:
                            pos = 12
                            aux = re.sub('[^0-9]', '', data[6])
                            try:
                                pos = int(aux)
                            except ValueError:
                                pos = 12
                        else:
                            pos = 0
                        emaitza = TaldeEmaitza(talde_izena=data[1],
                                               kalea=kalea, ziabogak=data[2:5],
                                               denbora=data[5], tanda=num + 1, posizioa=pos, tanda_postua=4)
                        self.estropada.taldeak_add(emaitza)
                except TypeError as e:
                    print(e)

    def calculate_tanda_posizioa(self):
        tanda_posizioak = [0] + [1] * 7
        for pos, taldea in enumerate(sorted(self.estropada.sailkapena)):
            taldea.posizioa = pos + 1
            taldea.tanda_postua = tanda_posizioak[taldea.tanda]
            tanda_posizioak[taldea.tanda] = tanda_posizioak[taldea.tanda] + 1

    def parse_resume(self, document):
        sailkapenak = document.cssselect('#resultado table')
        tandaKopurua = len(sailkapenak)
        rows = sailkapenak[tandaKopurua-1].findall('.//tr')
        tanda_posizioak = [0] + [1] * 7
        for pos, row in enumerate(rows):
            if pos == 0:
                continue
            try:
                taldea = row.find('.//td[2]').text.strip()
                posizioa = pos
                print(posizioa)
                puntuak = row.find('.//td[4]').text.strip()
                for t in self.estropada.sailkapena:
                    if re.match(t.talde_izena, taldea, re.I):
                        try:
                            t.posizioa = posizioa
                            t.tanda_postua = tanda_posizioak[t.tanda]
                            t.puntuazioa = int(puntuak)
                        except Exception as e:
                            print(e)
                            t.posizioa = 1
                            t.tanda_postua = tanda_posizioak[t.tanda]
                            t.puntuazioa = 0
                        tanda_posizioak[t.tanda] = tanda_posizioak[t.tanda] + 1
            except Exception as e:
                logging.warn(self.estropada.izena)
                logging.info("Error parsing results", exec_info=True)
