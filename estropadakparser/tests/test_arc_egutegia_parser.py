from estropadakparser.egutegia_parsers.arc_egutegia_parser import ArcEgutegiaParser


def test_arc_egutegia_parser():
    with open('./data/egutegia_arc_2022.html', encoding='utf-8') as file:
        content = file.read()
        parser = ArcEgutegiaParser('ARC1')
        estropadak = parser.parse(content)
        assert len(estropadak) == 14
        assert estropadak[0].izena == 'KEPA DEUN ARRANTZALEEN KOFRADIA XXII. IKURRIÑA'
        assert estropadak[0].data == '2022-06-19T00:00:00'
        assert estropadak[13].izena == 'XLIX IKURRIÑA VILLA DE BILBAO'
        assert estropadak[13].data == '2022-08-21T00:00:00'
