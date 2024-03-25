from estropadakparser.egutegia_parsers.act_egutegia_parser import ActEgutegiaParser


def test_act_egutegia_parser():
    with open('./data/egutegia_act_2024.html', encoding='utf-8') as file:
        content = file.read()
        parser = ActEgutegiaParser()
        estropadak = parser.parse(content)
        assert len(estropadak) == 22
        assert estropadak[0].izena == 'VIII Bandeira Cidade da Coruña'
        assert estropadak[0].data == '2024-06-29T00:00:00'
        assert estropadak[21].izena == 'Play-off J2'
        assert estropadak[21].data == '2024-09-15T00:00:00'
