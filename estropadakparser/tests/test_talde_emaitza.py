import pytest
from estropadakparser.estropada.estropada import TaldeEmaitza


def test_talde_emaitza():
    izena = 'Donostiarra'
    te = TaldeEmaitza(izena)
    assert type(te) == TaldeEmaitza
    assert te.talde_izena == izena


@pytest.mark.parametrize("test_input,expected", [
    (TaldeEmaitza('Donostiarra'),
     '{:30}'.format('Donostiarra')),
    (TaldeEmaitza('Donostiarra', **{'tanda': 1, 'kalea': 1}),
     '{:1}{:1}{:30}'.format(1, 1, 'Donostiarra')),
    (TaldeEmaitza('Donostiarra', **{'posizioa': 1, 'tanda': 1, 'kalea': 1}),
     '[{:2}]{:1}{:1}{:30}'.format(1, 1, 1, 'Donostiarra')),
    (TaldeEmaitza('Donostiarra', **{'posizioa': 1, 'tanda': 1, 'kalea': 1, 'ziabogak': ['04:50', '09:50', '14:50']}),
     '[{:2}]{:1}{:1}{:30}{:25}'.format(1, 1, 1, 'Donostiarra', ' '.join(['04:50', '09:50', '14:50']))),
    (TaldeEmaitza('Donostiarra', **{
        'posizioa': 1,
        'tanda': 1,
        'kalea': 1,
        'ziabogak': ['04:50', '09:50', '14:50'],
        'tanda_postua': 1,
        'denbora': '20:00.00'
        }),
     '[{:2}]{:1}{:1}{:1}{:30}{:25}{:8}'.format(1, 1, 1, 1, 'Donostiarra', ' '.join(['04:50', '09:50', '14:50']), '20:00.00')),
])
def test_print_talde_emaitza(test_input, expected):
    assert test_input.__repr__() == expected
