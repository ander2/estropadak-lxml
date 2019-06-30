from estropadakparser.egutegia_parsers.ete_egutegia_parser import EteEgutegiaParser

def test_ete_egutegia_parser():
    with open('./estropadakparser/tests/data/egutegia_ete_2018.html', encoding='utf-8') as file:
        content = file.read()
        parser = EteEgutegiaParser()
        estropadak = parser.parse(content)
        assert len(estropadak) == 14
        assert estropadak[0].izena == 'I. BANDERA ETE - PORTUGALETE'
        assert estropadak[0].data == '2018-06-17'
        assert estropadak[13].izena == 'COLINDRES'
        assert estropadak[13].data == '2018-08-25'