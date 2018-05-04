# coding=utf-8
import lxml.html
import re
import logging
import datetime
import urllib

from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza


class Parser(object):

    def __init__(self):
        pass

    def get_content(self, *args):
        '''Get content from URL or HTML string'''
        urla = args[0]
        if len(args) == 2 and args[1] is not None:
            document = lxml.html.fromstring(args[1])
        else:
            html_file = urllib.request.urlopen(urla)
            content = html_file.read()
            document = lxml.html.fromstring(content)
        return document


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
        self.parse_resume(document)
        return self.estropada

    def parse_headings(self, document):
        '''Parse table headings'''
        heading_three = document.cssselect('h3')
        data = ''
        if len(heading_three) > 0:
            name = heading_three[0].text.strip()
            heading = re.search('([^\(]*?)\(([^\)]*?)\)', name)
            estropada = heading.group(1).strip()
            data = heading.group(2)
        heading_table = document.cssselect('table[summary="Regata Puntuable"] td')
        lekua = ''
        if heading_table:
            lekua = heading_table[1].text.strip()
            ordua = heading_table[3].text.strip().replace('.', ':')
        data = data + ' ' + ordua
        return (estropada, data, lekua)

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
            if num == 0:
                posizioa = row.find('.//td[1]//span').text.strip()
            else:
                posizioa = row.find('.//td[1]').text.strip()
            team = row.find('.//td[2]').text.strip()
            puntuak = row.find('.//td[7]').text.strip()
            for taldea in self.estropada.sailkapena:
                if taldea.talde_izena == team:
                    try:
                        taldea.posizioa = int(posizioa)
                        taldea.puntuazioa = int(puntuak)
                    except:
                        print("Errorea")
                        taldea.posizioa = 1


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


class EuskotrenParser(Parser):
    '''Base class to parse an Euskotren race result'''

    def __init__(self):
        pass

    def parse(self, *args):
        '''Parse a result and return an estropada object'''
        urla = args[0]
        document = self.get_content(*args)
        (estropadaName, estropadaDate) = self.parse_headings(document)
        opts = {'urla': urla}
        self.estropada = Estropada(estropadaName, **opts)
        self.estropada.data = estropadaDate
        self.estropada.liga = 'euskotren'
        self.parse_tandas(document)
        self.parse_resume(document)
        return self.estropada

    def parse_headings(self, document):
        '''Parse headings table'''
        heading_three = document.cssselect('h3')
        name = heading_three[0].text_content().strip()
        heading = re.search('([^\(]*?)\(([^\)]*?)\)', name)
        estropada = heading.group(1).strip()
        data = heading.group(2)
        return (estropada, data)

    def parse_tandas(self, document):
        numberOfHeats = document.find_class('tabla_2')
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
                                              tanda_postua=resultData[6],
                                              posizioa=0)
                    self.estropada.taldeak_add(teamResult)

    def parse_resume(self, document):
        sailkapena = document.find_class('tabla')
        if len(sailkapena) > 0:
            rows = sailkapena[0].findall('.//tbody//tr')

            for row in rows:
                position = row.find('.//td[1]//span').text.strip()
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


class EstropadakParser(object):
    '''Factory class that returns the right parser
    based on the league name '''
    parsers = {'act': ActParser, 'arc': ArcParser, 'euskotren':
               EuskotrenParser, 'arc-legacy': ArcParserLegacy}

    def __new__(cls, league):
        return cls.parsers[league]()

    @classmethod
    def register(cls, league, parser):
        cls.parsers[league] = parser


class ActEgutegiaParser(object):
    '''Base class to parse the ACT calendar'''

    def __init__(self):
        self.document = ''
        self.estropada = None

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
            urla = 'http://www.euskolabelliga.com' + link
            opts = { 'urla': urla, 'data': data, 'lekua': lekua, 'liga': 'ACT'}
            estropada = Estropada(izena, **opts)
            estropadak.append(estropada)
        return estropadak


class ArcEgutegiaParser(object):
    '''Base class to parse the ARC1/ARC2 calendar'''

    def __init__(self, liga):
        self.document = ''
        self.estropada = None
        self.liga = liga

    def parse_date(self, date):
        new_date = date.replace('Junio', '06')
        new_date = new_date.replace('Julio', '07')
        new_date = new_date.replace('Agosto', '08')
        new_date = new_date.replace('Septiembre', '09')
        date_list = re.split(' ', new_date)
        if len(date_list) == 3:
            new_date = date_list[2] + "-" + date_list[1] + "-" + date_list[0]
        return new_date

    def parse(self, content):
        self.document = lxml.html.fromstring(content)
        if self.liga == 'ARC1':
            selector = 'tr.tab-item.g1'
        else:
            selector = 'tr.tab-item.g2'
        estropadak = []
        table_rows = self.document.cssselect(selector)
        for i, row in enumerate(table_rows):
            anchor = row.cssselect('a')
            izena = anchor[0].text.strip()
            link = anchor[0].attrib['href']
            lek_data = row.cssselect('.fecha span')
            data = self.parse_date(lek_data[0].text.strip() + ' 2017')
            opts = { 'urla': link, 'data': data, 'liga': self.liga}
            estropada = Estropada(izena, **opts)
            estropadak.append(estropada)
        return estropadak


class EuskotrenEgutegiaParser(Parser):
    '''Base class to parse the Euskotren calendar'''

    def __init__(self):
        self.document = ''
        self.estropada = None

    def parse(self, *args):
        urla = args[0]
        document = self.get_content(*args)
        self.liga = 'euskotren'
        selector = '.tabla_2 tbody tr'
        estropadak = []
        table_rows = document.cssselect(selector)
        for i, row in enumerate(table_rows):
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
