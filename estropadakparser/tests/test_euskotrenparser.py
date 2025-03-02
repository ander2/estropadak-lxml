import re
from estropadakparser.parsers.euskotrenparser import EuskotrenParser

base_url = 'http://www.euskolabelliga.com'


def test_euskotren_emaitzak_parser():
    euskotren_url = (f'{base_url}/femenina/resultados/'
                     'ver.php?id=eu&r=1395519778')
    euskotrenParser = EuskotrenParser()
    estropada = euskotrenParser.parse(euskotren_url)
    assert str(estropada) == 'V Bandera Marina de Cudeyo (2014-07-12 16:30)'
    assert estropada.urla == euskotren_url
    talde_kopurua = len(estropada.sailkapena)
    for taldea in estropada.sailkapena:
        assert taldea.posizioa in range(1, talde_kopurua + 1)
        assert taldea.puntuazioa in range(0, 8)
        assert taldea.kalea in range(1, 5)
        assert taldea.tanda in range(1, 2)
        assert re.match(r'\d{1,2}:\d{2}', taldea.ziabogak[0])
        assert re.match(r'\d{2}:\d{2},\d{2}', taldea.denbora)
