# coding=utf-8
import lxml.html
import re
from estropada import Estropada, TaldeEmaitza


class ActParser(object):
    '''Base class to parse an ACT race result'''

    def __init__(self):
        self.document = ''
        self.estropada = None

    def parse(self, content, estropada, estropada_id=0):
        '''Parse a result and return an estropada object'''
        self.document = lxml.html.fromstring(content)
        (estropadaName, estropadaDate) = self.parse_headings()
        self.estropada = Estropada(estropadaName, estropada_id)
        print estropadaDate
        print estropadaName
        self.estropada.mydate = estropadaDate
        self.estropada.liga = 'ACT'
        self.parse_tandas()
        self.parse_resume()
        return self.estropada

    def parse_headings(self):
        '''Parse headings table'''
        heading_three = self.document.cssselect('h3')
        name = heading_three[0].text.strip()
        heading = re.search('([^\(]*?)\(([^\)]*?)\)', name)
        estropada = heading.group(1).strip()
        data = heading.group(2)
        return (estropada, data)

    def parse_tandas(self):
        '''Parse race's paces tables'''
        tandas = self.document.find_class('tabla_tanda')
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

    def parse_resume(self):
        '''Parse race's resume table'''
        rank_table = '//table[@summary="Estropadaren sailkapena"]'
        sailkapena = self.document.xpath(rank_table)
        rows = sailkapena[-1].findall('.//tbody//tr')
        for num, row in enumerate(rows):
            if num == 0:
                posizioa = row.find('.//td[1]//span').text.strip()
            else:
                posizioa = row.find('.//td[1]').text.strip()
            team = row.find('.//td[2]').text.strip()
            puntuak = row.find('.//td[7]').text.strip()
            for taldea in self.estropada.taldeak:
                if taldea.talde_izena == team:
                    try:
                        taldea.posizioa = int(posizioa)
                        taldea.puntuazioa = int(puntuak)
                    except:
                        print "Errorea"
                        taldea.posizioa = 1


class ArcParser(object):
    '''Base class to parse an ARC race result'''

    def __init__(self):
        pass

    def parse(self, content, estropada, estropada_id=0):
        '''Parse a result and return an estropada object'''
        self.document = lxml.html.fromstring(content)
        (estropadaName, estropadaDate) = self.parse_headings()
        self.estropada = Estropada(estropadaName, estropada_id)
        self.estropada.mydate = estropadaDate
        self.estropada.liga = 'ARC'
        self.parse_tandas()
        self.parse_resume()
        return self.estropada

    def parse_headings(self):
        '''Parse headings table'''
        heading_two = self.document.cssselect('.resultado h2')
        estropada = heading_two[0].text.strip()
        date_block = self.document.cssselect('li.fecha')
        hour_block =  self.document.cssselect('li.hora')
        date = date_block[0].text_content().strip(" \n").replace('Fecha', '').strip(" \n")
        new_date = self.parse_date(date)
        hour = hour_block[0].text_content().replace('Hora', '').strip()
        race_date = new_date + " " + hour
        return (estropada, race_date)

    def parse_date(self, date):
        new_date = date.replace('Jun', '06')
        new_date = new_date.replace('Jul', '07')
        new_date = new_date.replace('Ago', '08')
        new_date = new_date.replace('Sept', '09')
        date_list = re.split(' ', new_date)
        new_date = date_list[2] +  "-" + date_list[1] +  "-" + date_list[0]
        return new_date

    def parse_tandas(self):
        tandas = self.document.cssselect('table.tanda')
        for num, text in enumerate(tandas):
            rows = text.findall('.//tbody//tr')
            for kalea, row in enumerate(rows):
                data = [x.text for x in row.findall('.//td')]
                taldea = row.find('.//span//a')
                emaitza = TaldeEmaitza(talde_izena=taldea.text.strip(),
                                       kalea=kalea + 1, ziabogak=data[1:4],
                                       denbora=data[4], tanda=num + 1)
                self.estropada.taldeak_add(emaitza)

    def parse_resume(self):
        sailkapena = self.document.find_class('clasificacion-regata')
        rows = sailkapena[0].findall('.//tbody//tr')
        tanda_posizioak = [0] + [1] * 5
        for pos, row in enumerate(rows):
            taldea = row.find('.//span//a').text.strip()
            try:
                puntuak = row.find('.//td[3]').text.strip()
            except:
                puntuak = 0
            for t in self.estropada.taldeak:
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


class EuskotrenParser(object):
    '''Base class to parse an Euskotren race result'''

    def __init__(self):
        pass

    def parse(self, content, estropada, estropada_id=0):
        '''Parse a result and return an estropada object'''
        self.document = lxml.html.fromstring(content)
        self.estropada = Estropada(estropada, estropada_id)
        self.numberOfHeats = self.document.find_class('tabla_2')
        self.parse_tandas()
        self.parse_resume()
        return self.estropada

    def parse_tandas(self):
        for num, heat in enumerate(self.numberOfHeats):
            results = heat.findall('.//tbody//tr')
            for result in results:
                resultData = [x.text for x in result.findall('.//td')]
                teamName = resultData[1].strip()
                ziabogak = map(lambda s: s or '', resultData[2:5])
                teamResult = TaldeEmaitza(talde_izena=teamName,
                                          kalea=int(resultData[0]),
                                          ziabogak=ziabogak,
                                          denbora=resultData[5], tanda=num + 1,
                                          tanda_postua=resultData[6],
                                          posizioa=0)
                self.estropada.taldeak_add(teamResult)

    def parse_resume(self):
        sailkapena = self.document.find_class('tabla')
        rows = sailkapena[0].findall('.//tbody//tr')

        for row in rows:
            position = row.find('.//td[1]//span').text.strip()
            teamName = row.find('.//td[2]').text.strip()
            puntuazioa = row.find('.//td[7]').text.strip()
            for t in self.estropada.taldeak:
                if t.talde_izena == teamName:
                    try:
                        t.posizioa = int(position)
                        t.puntuazioa = int(puntuazioa)
                    except:
                        print "Errorea"
                        t.posizioa = 1


class EstropadakParser(object):
    '''Factory class that returns the right parser
    based on the league name '''
    parsers = {'act': ActParser, 'arc': ArcParser, 'euskotren':
               EuskotrenParser}

    def __new__(cls, league):
        return cls.parsers[league]()
