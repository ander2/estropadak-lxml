#coding utf-8
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
        estropadaName = self.parse_headings()
        self.estropada = Estropada(estropadaName, estropada_id)
        self.parse_tandas()
        self.parse_resume()
        return self.estropada

    def parse_headings(self):
        '''Parse headings table'''
        heading_three = self.document.cssselect('h3')
        name = heading_three[0].text.strip()
        heading = re.search('([^\(]*?)(\([^\)]*?\))', name)
        estropada = heading.group(1).strip()
        return estropada

    def parse_tandas(self):
        '''Parse race's paces tables'''
        tandas = self.document.find_class('tabla_tanda')
        for num, text in enumerate(tandas):
            rows = text.findall('.//tbody//tr')
            for row in rows:
                data = [x.text for x in row.findall('.//td')]
                kalea = int(data[0])
                emaitza = TaldeEmaitza(talde_izena=data[1].strip(),
                        kalea=kalea, ziabogak=data[2:5], denbora=data[5],
                        tanda=num + 1, tanda_postua=data[6], posizioa=0)
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
        self.estropada = Estropada(estropada, estropada_id)
        self.parse_tandas()
        self.parse_resume()
        return self.estropada

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

    def __init__(self, url):
        self.url = url

    @classmethod
    def parse(self, content, estropada, estropada_id=0):
        '''Parse a result and return an estropada object'''
        document = lxml.html.fromstring(content)
        tandas = document.find_class('tabla_2')
        estropada = Estropada(estropada, estropada_id)
        for num, text in enumerate(tandas):
            rows = text.findall('.//tbody//tr')
            for row in rows:
                data = [x.text for x in row.findall('.//td')]
                team = data[1].strip()
                ziabogak = map(lambda s: s or '', data[2:5])
                emaitza = TaldeEmaitza(talde_izena=team,
                        kalea=data[0], ziabogak=ziabogak, denbora=data[5],
                        tanda=num + 1, tanda_postua=data[6], posizioa=0)
                estropada.taldeak_add(emaitza)
        sailkapena = document.find_class('tabla')
        rows = sailkapena[0].findall('.//tbody//tr')

        for row in rows:
            pos = row.find('.//td[1]//span').text.strip()
            team = row.find('.//td[2]').text.strip()
            puntuazioa = row.find('.//td[7]').text.strip()
            for t in estropada.taldeak:
                if t.talde_izena == team:
                    try:
                        t.posizioa = int(pos)
                        t.puntuazioa = int(puntuazioa)
                    except:
                        print "Errorea"
                        t.posizioa = 1
        return estropada


class EstropadakParser(object):
    '''Factory class that returns the right parser
    based on the league name '''
    parsers = {'act': ActParser, 'arc': ArcParser, 'euskotren':
               EuskotrenParser}

    def __new__(cls, league):
        if league == 'act':
            return ActParser()
        else:
            return cls.parsers[league]()
