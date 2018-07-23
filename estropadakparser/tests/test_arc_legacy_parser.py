import re
from estropadakparser.parsers.arc_legacy_parser import ArcParserLegacy
from estropadakparser.estropada.estropada import Estropada

def test_parse_arc_legacy():
    url = 'http://www.liga-arc.com/historico/resultados_detalle.php?id=123'
    arcParser = ArcParserLegacy()
    estropada = arcParser.parse(url, None, '2007-06-30','ARC1')
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