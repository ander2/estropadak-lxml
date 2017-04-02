import urllib.request
import re
from estropadakparser.estropadakparser import EstropadakParser
from estropadakparser.estropada.estropada import Estropada


def test_parse_arc():
    url = 'http://www.euskolabelliga.com/resultados/ver.php?id=eu&r=1084290925'
    file = urllib.request.urlopen(url)
    content = file.read()
    estropada = EstropadakParser('act').parse(content, None)
    assert isinstance(estropada, Estropada)
    talde_kopurua = len(estropada.taldeak)
    assert talde_kopurua == 12
    assert estropada.lekua == 'Arriluze  Getxo Bizkaia'
    for taldea in estropada.taldeak:
        assert type(taldea.posizioa) == int
        assert taldea.posizioa in range(1, talde_kopurua + 1)
        assert type(taldea.puntuazioa) == int
        assert taldea.puntuazioa in range(0, 13)
        assert type(taldea.kalea) == int
        assert taldea.kalea in range(1, 5)
        assert type(taldea.tanda) == int
        assert taldea.tanda in range(1, 4)
        for ziab in taldea.ziabogak:
            assert re.match('\d{1,2}:\d{2}', ziab)
        assert re.match('\d{2}:\d{2},\d{2}', taldea.denbora)

def test_parse_arc_legacy():
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

#    def test_parse_arc2(self):
#        self.estropada = EstropadakParser('arc').parse(self.arc2RaceHtml,
#                                                       None)
#        self.assertIsInstance(self.estropada, Estropada, 'Not a estropada')
#        talde_kopurua = len(self.estropada.taldeak)
#        for taldea in self.estropada.taldeak:
#            self.assertIs(type(taldea.posizioa), int)
#            self.assertIn(taldea.posizioa, range(1, talde_kopurua + 1))
#            self.assertIs(type(taldea.puntuazioa), int)
#            self.assertIn(taldea.puntuazioa, range(0, 15))
#            self.assertIs(type(taldea.kalea), int)
#            self.assertIn(taldea.kalea, range(1, 5))
#            self.assertIs(type(taldea.tanda), int)
#            self.assertIn(taldea.tanda, range(1, 5))
#            for ziab in taldea.ziabogak:
#                self.assertRegexpMatches(ziab, '\d{1,2}:\d{2}')
#            self.assertRegexpMatches(taldea.denbora, '\d{2}:\d{2},\d{2}')
     
