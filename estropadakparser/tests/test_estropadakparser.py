import re
from estropadakparser.estropadakparser import EstropadakParser
from estropadakparser.parsers.actparser import ActParser

base_url = 'http://www.euskolabelliga.com'


def test_register_parser():
    act_url = (f'{base_url}/resultados/'
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
