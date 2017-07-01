import unittest
import urllib.request
import re
from estropadakparser.estropadakparser import EstropadakParser
from estropadakparser.estropada.estropada import Estropada


class TestEstropadakParser(unittest.TestCase):
    '''Test class for testing EstropadakParser class'''
    def setUp(self):
        act_url = ('http://www.ligasanmiguel.com/resultados/'
                            'ver.php?id=eu&r=1365765288')
        actRaceResult = urllib.request.urlopen(act_url)
        self.actRaceHtml = actRaceResult.read()
        self.actEstropadaName = 'Bandera Euskadi Basque Country'
        self.estropadaId = 'Id'
        arc1_url = ('http://www.liga-arc.com/es/regata/163/'
        'xxiii-bandera-ayuntamiento-de-camargo')
        arc1RaceResult = urllib.request.urlopen(arc1_url)
        self.arc1RaceHtml = arc1RaceResult.read()
        arc2_url = ('http://www.liga-arc.com/es/regata/172/'
                   'xli-bandera-ciudad-de-castro-vi-mem.-avelino-ibaez')
        arc2RaceResult = urllib.request.urlopen(arc2_url)
        self.arc2RaceHtml = arc2RaceResult.read()
        euskotren_url = ('http://www.ligasanmiguel.com/femenina/resultados/'
                         'ver.php?id=es&r=1395519778')
        euskotrenRaceResult = urllib.request.urlopen(euskotren_url)
        self.euskotrenRaceHtml = euskotrenRaceResult.read()

    def test_parse_act(self):
        self.estropada = EstropadakParser('act').parse(self.actRaceHtml,
                                                       None)
        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
        self.assertEqual(self.estropada.izena, 'Bandera Euskadi Basque Country')
        self.assertEqual(len(self.estropada.taldeak), 12)
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
        self.estropada = EstropadakParser('arc').parse(self.arc1RaceHtml,
                                                       None)
        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
        self.assertIs(self.estropada.liga, 'ARC1')
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
        self.estropada = EstropadakParser('arc').parse(self.arc2RaceHtml,
                                                       None)
        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
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
        file = urllib.request.urlopen(url)
        content = file.read()
        estropada = EstropadakParser('arc-legacy').parse(content,
                                          None, '2007-06-30')
        assert isinstance(estropada, Estropada)
        talde_kopurua = len(estropada.taldeak)
        assert talde_kopurua == 12
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
        self.estropada = EstropadakParser('euskotren').parse(self.euskotrenRaceHtml, None)
        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
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
