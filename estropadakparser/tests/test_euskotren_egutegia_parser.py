from estropadakparser.egutegia_parsers.euskotren_egutegia_parser import EuskotrenEgutegiaParser

def test_euskotren_egutegia_parser():
    # http://www.euskolabelliga.com/femenina/calendario/index.php?id=es&t=2017
    with open('./data/egutegia_euskotren_2017.html', encoding='iso-8859-1') as file:
        content = file.read()
        parser = EuskotrenEgutegiaParser()
        estropadak = parser.parse(content)
        assert len(estropadak) == 8
        assert estropadak[0].izena == 'V. Orio Kanpina Bandera'
        assert estropadak[0].lekua == 'Orio'
        assert estropadak[0].data == '2017-07-08'
        assert estropadak[7].izena == 'Zarauzko IX Ikurriña J2'
        assert estropadak[7].lekua == 'Zarautz'
        assert estropadak[7].data == '2017-08-20'
