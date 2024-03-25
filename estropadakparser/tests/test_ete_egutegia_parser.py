from estropadakparser.egutegia_parsers.ete_egutegia_parser import EteEgutegiaParser


def test_ete_egutegia_parser():
    with open('./data/egutegia_ete_2018.html', encoding='utf-8') as file:
        content = file.read()
        parser = EteEgutegiaParser()
        estropadak = parser.parse(content)
        assert len(estropadak) == 14
        assert estropadak[0].izena == 'I. BANDERA ETE - PORTUGALETE'
        assert estropadak[0].data == '2018-06-17T00:00:00'
        assert estropadak[13].izena == 'III BANDERA FEMENINA DE TRAINERAS AYUNTAMIENTO DE COLINDRES'
        assert estropadak[13].data == '2018-08-25T00:00:00'
