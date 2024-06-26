import datetime
import logging
import re
from estropadakparser.parsers.parser import Parser
from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza


class EuskotrenParser(Parser):
    '''Base class to parse an Euskotren race result'''

    def __init__(self):
        pass

    def parse(self, *args):
        '''Parse a result and return an estropada object'''
        urla = args[0]
        document = self.get_content(*args)
        (estropadaName, estropadaDate, lekua) = self.parse_headings(document)
        opts = {'urla': urla, 'lekua': lekua, 'data': estropadaDate, 'liga': 'euskotren'}
        self.estropada = Estropada(estropadaName, **opts)
        self.parse_tandas(document)
        self.parse_resume(document)
        return self.estropada

    def parse_headings(self, document):
        '''Parse headings table'''
        heading_three = document.cssselect('h3')
        data = ''
        if len(heading_three) > 0:
            name = heading_three[0].text.strip()
            estropada = name.split('(')[0].strip()
            quoted_text = re.findall('\(([^\)]+)', name)
            for t in quoted_text:
                for data_format in ['%Y-%m-%d', '%d-%m-%Y']:
                    try:
                        data = datetime.datetime.strptime(t, data_format)
                    except ValueError:
                        pass
                if data == '':
                    estropada = estropada + t
        heading_table = document.cssselect('table[summary="Regata Puntuable"] td')
        lekua = ''
        if heading_table:
            lekua = heading_table[1].text.strip()
            ordua = re.split('[.:]', heading_table[3].text.strip())
            if len(ordua) > 1:
                data = data.replace(hour=int(ordua[0], 10), minute=int(ordua[1], 10))
        data_text = data.isoformat()
        return (estropada, data_text, lekua)

    def parse_tandas(self, document):
        numberOfHeats = document.find_class('tabla_tanda')
        for num, heat in enumerate(numberOfHeats):
            results = heat.findall('.//tbody//tr')
            for result in results:
                resultData = [x.text for x in result.findall('.//td')]
                if resultData[1] is not None:
                    teamName = resultData[1].strip()
                    # ziabogak = map(lambda s: s or '', resultData[2:5])
                    ziabogak = [result if result is not None else '' for result in resultData[2:5]]
                    if resultData[5] is None:
                        denbora = ''
                    else:
                        denbora = resultData[5]
                    teamResult = TaldeEmaitza(talde_izena=teamName,
                                              kalea=int(resultData[0]),
                                              ziabogak=ziabogak,
                                              denbora=denbora, tanda=num + 1,
                                              tanda_postua=int(resultData[6]),
                                              posizioa=0)
                    self.estropada.taldeak_add(teamResult)

    def parse_resume(self, document):
        sailkapena = document.cssselect('h3.clasificacion + .fondo_taula > .taula')
        if len(sailkapena) > 0:
            rows = sailkapena[0].findall('.//tbody//tr')

            for row in rows:
                position = row.find('.//td[1]').text_content()
                teamName = row.find('.//td[2]').text
                if teamName is not None:
                    teamName = row.find('.//td[2]').text.strip()
                    puntuazioa = row.find('.//td[7]').text.strip()
                    for t in self.estropada.sailkapena:
                        if t.talde_izena == teamName:
                            try:
                                t.posizioa = int(position)
                                t.puntuazioa = int(puntuazioa)
                            except:
                                print("Errorea")
                                t.posizioa = 1
