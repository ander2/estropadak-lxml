import pytest
import urllib.request
import re
from estropadakparser.estropadakparser import EstropadakParser
from estropadakparser.parsers.actparser import ActParser
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
    parser = EstropadakParser('actt')
    estropada = parser.parse(act_url)
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
