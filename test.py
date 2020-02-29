from estropadakparser.estropadakparser import EstropadakParser


url = 'http://www.euskolabelliga.com/resultados/ver.php?id=eu&r=1521890221'
estropada = EstropadakParser('act').parse(url)
estropada.dump_json()
