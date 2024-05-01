import re
from estropadakparser.parsers.arcparser import ArcParser


def test_parse_arc1():
    arc1_url = ('http://www.liga-arc.com/es/regata/163/'
                'xxiii-bandera-ayuntamiento-de-camargo')
    arcParser = ArcParser()
    estropada = arcParser.parse(arc1_url)
    assert str(estropada) == 'XXIII Bandera Ayuntamiento de Camargo (2013-08-24 18:15)'
    assert estropada.liga == 'ARC1'
    assert estropada.data == '2013-08-24T18:15:00'
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
    arcParser = ArcParser()
    estropada = arcParser.parse(arc2_url)
    assert str(estropada) == 'XLI Bandera Ciudad de Castro-VI Mem. Avelino Ibañez (2013-08-15 18:00)'
    assert estropada.data == '2013-08-15T18:00:00'
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