import re
from estropadakparser.parsers.eteparser import EteParser

def test_parse_ete():
    ete_url = ('https://www.ligaete.com/es/regata/'
               '356/emakumeen-i.-orio-kanpina-bandera')
    eteParser = EteParser()
    estropada = eteParser.parse(ete_url)
    assert str(estropada) == 'EMAKUMEEN I. ORIO KANPINA BANDERA (2018-07-21 11:00)'
    assert estropada.liga == 'ETE'
    assert estropada.urla == ete_url
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
