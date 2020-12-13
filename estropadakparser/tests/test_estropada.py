from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza


def test_estropada():
    izena = 'Test estropada'
    e = Estropada(izena)
    assert type(e) == Estropada
    assert e.izena == izena


def test_estropada_with_common_props():
    izena = 'Test estropada'
    props = {
        'lekua': 'Donostia',
        'liga': 'ACT',
        'data': '2020-06-01 17:00'
    }
    e = Estropada(izena, **props)
    assert type(e) == Estropada
    assert e.izena == izena
    assert e.lekua == props['lekua']
    assert e.liga == props['liga']
    assert e.data == props['data']


def test_estropada_with_sailkapena_with_dicts():
    izena = 'Test estropada'
    props = {
        'sailkapena': [{
            'talde_izena': 'Hondarribia',
            'kalea': 1,
            'tanda': 1
        }, {
            'talde_izena': 'Urdaibai',
            'kalea': 2,
            'tanda': 1
        }]
    }
    e = Estropada(izena, **props)
    assert type(e) == Estropada
    assert e.izena == izena
    assert len(e.sailkapena) == 2
    assert type(e.sailkapena[0]) == TaldeEmaitza
    assert e.sailkapena[0].talde_izena == 'Hondarribia'
    assert e.sailkapena[1].talde_izena == 'Urdaibai'


def test_estropada_with_sailkapena_with_team_emaitza_objects():
    izena = 'Test estropada'
    props = {
        'sailkapena': [
            TaldeEmaitza('Hondarribia', **{'kalea': 1, 'tanda': 1}),
            TaldeEmaitza('Urdaibai', **{'kalea': 2, 'tanda': 1})
        ]
    }
    e = Estropada(izena, **props)
    assert type(e) == Estropada
    assert e.izena == izena
    assert len(e.sailkapena) == 2
    assert type(e.sailkapena[0]) == TaldeEmaitza
    assert e.sailkapena[0].talde_izena == 'Hondarribia'
    assert e.sailkapena[1].talde_izena == 'Urdaibai'
