import re
from estropadakparser.parsers.actparser import ActParser

base_url = 'http://www.euskolabelliga.com'


def test_parse_act():
    act_url = (f'{base_url}/resultados/'
               'ver.php?id=eu&r=1365765288')
    actParser = ActParser()
    estropada = actParser.parse(act_url)
    assert str(estropada) == 'Bandera Euskadi Basque Country (2013-06-16 12:00)'
    assert estropada.izena == 'Bandera Euskadi Basque Country'
    assert estropada.data == '2013-06-16T12:00:00'
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
    act_url = (f'{base_url}/resultados'
               '/ver.php?id=eu&r=1521889449')
    actParser = ActParser()
    estropada = actParser.parse(act_url)
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


def test_parse_act_ez_puntuagarria():
    act_url = ('https://www.euskolabelliga.com/resultados/ver.php?id=es&r=1110968398')
    actParser = ActParser()
    estropada = actParser.parse(act_url)
    assert estropada.puntuagarria is False
