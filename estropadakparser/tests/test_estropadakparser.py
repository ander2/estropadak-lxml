import unittest
import pytest
import urllib.request
import re
from estropadakparser.estropadakparser import EstropadakParser
from estropadakparser.estropada.estropada import Estropada


class TestEstropadakParser(unittest.TestCase):
    '''Test class for testing EstropadakParser class'''
    def setUp(self):
        arc1_url = ('http://www.liga-arc.com/es/regata/163/'
                    'xxiii-bandera-ayuntamiento-de-camargo')
        arc2_url = ('http://www.liga-arc.com/es/regata/172/'
                    'xli-bandera-ciudad-de-castro-vi-mem.-avelino-ibaez')
        arc2RaceResult = urllib.request.urlopen(arc2_url)
        self.arc2RaceHtml = arc2RaceResult.read()
        euskotren_url = ('http://www.ligasanmiguel.com/femenina/resultados/'
                         'ver.php?id=es&r=1395519778')
        euskotrenRaceResult = urllib.request.urlopen(euskotren_url)
        self.euskotrenRaceHtml = euskotrenRaceResult.read()

    def test_parse_act(self):
        act_url = ('http://www.ligasanmiguel.com/resultados/'
                   'ver.php?id=eu&r=1365765288')
        kwargs = {'urla': act_url}
        self.estropada = EstropadakParser('act').parse(act_url)
        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
        self.assertEqual(self.estropada.izena, 'Bandera Euskadi Basque Country')
        self.assertEqual(len(self.estropada.taldeak), 12)
        assert self.estropada.urla == act_url
        for taldea in self.estropada.taldeak:
            self.assertIs(type(taldea.posizioa), int)
            self.assertIn(taldea.posizioa, range(1, 13))
            self.assertIs(type(taldea.puntuazioa), int)
            self.assertIn(taldea.puntuazioa, range(1, 13))
            self.assertIs(type(taldea.kalea), int)
            self.assertIn(taldea.kalea, range(1, 5))
            self.assertIs(type(taldea.tanda), int)
            self.assertIn(taldea.tanda, range(1, 4))
            for ziab in taldea.ziabogak:
                self.assertRegexpMatches(ziab, '\d{2}:\d{2}')
            self.assertRegexpMatches(taldea.denbora, '\d{2}:\d{2},\d{2}')

    def test_parse_arc1(self):
        arc1_url = ('http://www.liga-arc.com/es/regata/163/'
                    'xxiii-bandera-ayuntamiento-de-camargo')
        kwargs = {'urla': arc1_url}
        self.estropada = EstropadakParser('arc').parse(arc1_url)
        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
        self.assertIs(self.estropada.liga, 'ARC1')
        assert self.estropada.urla == arc1_url
        talde_kopurua = len(self.estropada.taldeak)
        for taldea in self.estropada.taldeak:
            self.assertIs(type(taldea.posizioa), int)
            self.assertIn(taldea.posizioa, range(1, talde_kopurua + 1))
            self.assertIs(type(taldea.puntuazioa), int)
            self.assertIn(taldea.puntuazioa, range(1, 13))
            self.assertIs(type(taldea.kalea), int)
            self.assertIn(taldea.kalea, range(1, 5))
            self.assertIs(type(taldea.tanda), int)
            self.assertIn(taldea.tanda, range(1, 4))
            for ziab in taldea.ziabogak:
                self.assertRegexpMatches(ziab, '\d{1,2}:\d{2}')
            self.assertRegexpMatches(taldea.denbora, '\d{2}:\d{2},\d{2}')

    def test_parse_arc2(self):
        arc2_url = ('http://www.liga-arc.com/es/regata/172/'
                    'xli-bandera-ciudad-de-castro-vi-mem.-avelino-ibaez')
        self.estropada = EstropadakParser('arc').parse(arc2_url)
        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
        assert self.estropada.urla == arc2_url
        talde_kopurua = len(self.estropada.taldeak)
        for taldea in self.estropada.taldeak:
            self.assertIs(type(taldea.posizioa), int)
            self.assertIn(taldea.posizioa, range(1, talde_kopurua + 1))
            self.assertIs(type(taldea.puntuazioa), int)
            self.assertIn(taldea.puntuazioa, range(0, 15))
            self.assertIs(type(taldea.kalea), int)
            self.assertIn(taldea.kalea, range(1, 5))
            self.assertIs(type(taldea.tanda), int)
            self.assertIn(taldea.tanda, range(1, 5))
            for ziab in taldea.ziabogak:
                self.assertRegexpMatches(ziab, '\d{1,2}:\d{2}')
            self.assertRegexpMatches(taldea.denbora, '\d{2}:\d{2},\d{2}')

    def test_parse_arc_legacy(self):
        url = 'http://www.liga-arc.com/historico/resultados_detalle.php?id=123'
        estropada = EstropadakParser('arc-legacy').parse(url, None, '2007-06-30','ARC1')
        assert isinstance(estropada, Estropada)
        talde_kopurua = len(estropada.taldeak)
        assert talde_kopurua == 12
        assert estropada.urla == url
        for taldea in estropada.taldeak:
            assert type(taldea.posizioa) == int
            assert taldea.posizioa in range(1, talde_kopurua + 1)
            assert type(taldea.kalea) == int
            assert taldea.kalea in range(1, 5)
            assert type(taldea.tanda) == int
            assert taldea.tanda in range(1, 4)
            for ziab in taldea.ziabogak:
                assert re.match('\d{1,2}:\d{2}', ziab)
            assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora)

    def test_euskotren(self):
        euskotren_url = ('http://www.ligasanmiguel.com/femenina/resultados/'
                         'ver.php?id=es&r=1395519778')
        self.estropada = EstropadakParser('euskotren').parse(euskotren_url)
        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
        assert self.estropada.urla == euskotren_url
        talde_kopurua = len(self.estropada.taldeak)
        for taldea in self.estropada.taldeak:
            self.assertIs(type(taldea.posizioa), int)
            self.assertIn(taldea.posizioa, range(1, talde_kopurua + 1))
            self.assertIs(type(taldea.puntuazioa), int)
            self.assertIn(taldea.puntuazioa, range(0, 8))
            self.assertIs(type(taldea.kalea), int)
            self.assertIn(taldea.kalea, range(1, 5))
            self.assertIs(type(taldea.tanda), int)
            self.assertIn(taldea.tanda, range(1, 2))
            self.assertRegexpMatches(taldea.ziabogak[0], '\d{1,2}:\d{2}')
            self.assertRegexpMatches(taldea.denbora, '\d{2}:\d{2},\d{2}')


if __name__ == 'main':
    unittest.main()
