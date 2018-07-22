import pytest
import urllib.request
import re
from estropadakparser.estropadakparser import EstropadakParser, EuskotrenEgutegiaParser, ActParser
from estropadakparser.estropada.estropada import Estropada


#    '''Test class for testing EstropadakParser class'''
#    def setUp(self):
#        arc1_url = ('http://www.liga-arc.com/es/regata/163/'
#                    'xxiii-bandera-ayuntamiento-de-camargo')
#        arc2_url = ('http://www.liga-arc.com/es/regata/172/'
#                    'xli-bandera-ciudad-de-castro-vi-mem.-avelino-ibaez')
#        arc2RaceResult = urllib.request.urlopen(arc2_url)
#        self.arc2RaceHtml = arc2RaceResult.read()
#        euskotren_url = ('http://www.ligasanmiguel.com/femenina/resultados/'
#                         'ver.php?id=es&r=1395519778')
#        euskotrenRaceResult = urllib.request.urlopen(euskotren_url)
#        self.euskotrenRaceHtml = euskotrenRaceResult.read()

def test_register_parser():
    act_url = ('http://www.ligasanmiguel.com/resultados/'
                'ver.php?id=eu&r=1365765288')
    EstropadakParser.register('actt', ActParser)
    estropada = EstropadakParser('actt').parse(act_url)
    assert str(estropada) == 'Bandera Euskadi Basque Country (2013-06-16 12:00)'
    assert estropada.izena == 'Bandera Euskadi Basque Country'
    assert len(estropada.sailkapena) == 12
    assert estropada.urla == act_url
    for taldea in estropada.sailkapena:
        assert type(taldea.posizioa) == int
        assert taldea.posizioa in range(1, 13)
        assert type(taldea.puntuazioa) == int
        assert taldea.puntuazioa in range(1, 13)
        assert type(taldea.kalea) == int
        assert taldea.kalea in range(1, 5)
        assert type(taldea.tanda) == int
        assert taldea.tanda in range(1, 4)
        for ziab in taldea.ziabogak:
            assert re.match('\d{2}:\d{2}', ziab) is not None
        assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora) is not None

def test_parse_act():
    act_url = ('http://www.ligasanmiguel.com/resultados/'
                'ver.php?id=eu&r=1365765288')
    kwargs = {'urla': act_url}
    estropada = EstropadakParser('act').parse(act_url)
    assert str(estropada) == 'Bandera Euskadi Basque Country (2013-06-16 12:00)'
    assert estropada.izena == 'Bandera Euskadi Basque Country'
    assert len(estropada.sailkapena) == 12
    assert estropada.urla == act_url
    for taldea in estropada.sailkapena:
        assert type(taldea.posizioa) == int
        assert taldea.posizioa in range(1, 13)
        assert type(taldea.puntuazioa) == int
        assert taldea.puntuazioa in range(1, 13)
        assert type(taldea.kalea) == int
        assert taldea.kalea in range(1, 5)
        assert type(taldea.tanda) == int
        assert taldea.tanda in range(1, 4)
        for ziab in taldea.ziabogak:
            assert re.match('\d{2}:\d{2}', ziab) is not None
        assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora) is not None

def test_parse_act_without_sailkapena():
    act_url = ('http://www.euskolabelliga.com/resultados'
                '/ver.php?id=eu&r=1521889449')
    kwargs = {'urla': act_url}
    estropada = EstropadakParser('act').parse(act_url)
    assert str(estropada) == 'Orioko XXVIII. Estropadak - VI. Orio Kanpina Bandera (2018-07-22 11:45)'
    assert estropada.izena == 'Orioko XXVIII. Estropadak - VI. Orio Kanpina Bandera'
    assert len(estropada.sailkapena) == 12
    assert estropada.urla == act_url
    for taldea in estropada.sailkapena:
        assert type(taldea.posizioa) == int
        assert taldea.posizioa in range(1, 13)
        if taldea.talde_izena == 'ORIO BABYAUTO':
            assert taldea.puntuazioa == 12
        assert type(taldea.puntuazioa) == int
        assert taldea.puntuazioa in range(1, 13)
        assert type(taldea.kalea) == int
        assert taldea.kalea in range(1, 5)
        assert type(taldea.tanda) == int
        assert taldea.tanda in range(1, 4)
        for ziab in taldea.ziabogak:
            assert re.match('\d{2}:\d{2}', ziab) is not None
        assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora) is not None


def test_parse_arc1():
    arc1_url = ('http://www.liga-arc.com/es/regata/163/'
                'xxiii-bandera-ayuntamiento-de-camargo')
    kwargs = {'urla': arc1_url}
    estropada = EstropadakParser('arc').parse(arc1_url)
    assert str(estropada) == 'XXIII Bandera Ayuntamiento de Camargo (2013-08-24 18:15)'
    assert estropada.liga == 'ARC1'
    assert estropada.urla == arc1_url
    talde_kopurua = len(estropada.sailkapena)
    for taldea in estropada.sailkapena:
        assert type(taldea.posizioa) == int
        assert taldea.posizioa in range(1, talde_kopurua + 1)
        assert type(taldea.puntuazioa) == int
        assert taldea.puntuazioa in range(1, 13)
        assert type(taldea.kalea) == int
        assert taldea.kalea in range(1, 5)
        assert type(taldea.tanda) == int
        assert taldea.tanda in range(1, 4)
        for ziab in taldea.ziabogak:
            assert re.match('\d{1,2}:\d{2}', ziab) is not None
        assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora) is not None

def test_parse_arc2():
    arc2_url = ('http://www.liga-arc.com/es/regata/172/'
                'xli-bandera-ciudad-de-castro-vi-mem.-avelino-ibaez')
    estropada = EstropadakParser('arc').parse(arc2_url)
    assert str(estropada) == 'XLI Bandera Ciudad de Castro-VI Mem. Avelino Ibañez (2013-08-15 18:00)'
    assert estropada.urla == arc2_url
    talde_kopurua = len(estropada.sailkapena)
    for taldea in estropada.sailkapena:
        assert type(taldea.posizioa) == int
        assert taldea.posizioa in range(1, talde_kopurua + 1)
        assert type(taldea.puntuazioa) == int
        assert taldea.puntuazioa in range(0, 15)
        assert type(taldea.kalea) == int
        assert taldea.kalea in range(1, 5)
        assert type(taldea.tanda) == int
        assert taldea.tanda in range(1, 5)
        for ziab in taldea.ziabogak:
            assert re.match('\d{1,2}:\d{2}', ziab) is not None
        assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora) is not None

def test_parse_arc_legacy():
    url = 'http://www.liga-arc.com/historico/resultados_detalle.php?id=123'
    estropada = EstropadakParser('arc-legacy').parse(url, None, '2007-06-30','ARC1')
    assert isinstance(estropada, Estropada)
    talde_kopurua = len(estropada.sailkapena)
    assert talde_kopurua == 12
    assert estropada.urla == url
    for taldea in estropada.sailkapena:
        assert type(taldea.posizioa) == int
        assert taldea.posizioa in range(1, talde_kopurua + 1)
        assert type(taldea.kalea) == int
        assert taldea.kalea in range(1, 5)
        assert type(taldea.tanda) == int
        assert taldea.tanda in range(1, 4)
        for ziab in taldea.ziabogak:
            assert re.match('\d{1,2}:\d{2}', ziab)
        assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora)

def test_euskotren_emaitzak_parser():
    euskotren_url = ('http://www.ligasanmiguel.com/femenina/resultados/'
                        'ver.php?id=es&r=1395519778')
    estropada = EstropadakParser('euskotren').parse(euskotren_url)
    assert str(estropada) == 'V Bandera Marina de Cudeyo (2014-07-12)'
    assert estropada.urla == euskotren_url
    talde_kopurua = len(estropada.sailkapena)
    for taldea in estropada.sailkapena:
        assert type(taldea.posizioa) == int
        assert taldea.posizioa in range(1, talde_kopurua + 1)
        assert type(taldea.puntuazioa) == int
        assert taldea.puntuazioa in range(0, 8)
        assert type(taldea.kalea) == int
        assert taldea.kalea in range(1, 5)
        assert type(taldea.tanda) == int
        assert taldea.tanda in range(1, 2)
        assert re.match('\d{1,2}:\d{2}', taldea.ziabogak[0])
        assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora)

def test_euskotren_egutegia_parser():
    euskotren_url = ('http://www.euskolabelliga.com/'
                        'femenina/calendario/index.php?id=es&t=2017')
    estropadak = EuskotrenEgutegiaParser().parse(euskotren_url)
    assert len(estropadak) == 8
    assert estropadak[0].izena == 'V. Orio Kanpina Bandera'
    assert estropadak[0].lekua == 'Orio'
    assert estropadak[0].data == '2017-07-08 17:30'
    assert estropadak[7].izena == 'Zarauzko IX Ikurriña J2'
    assert estropadak[7].lekua == 'Zarautz'
    assert estropadak[7].data == '2017-08-20 12:00'
