import urllib.request
from estropadakparser.egutegia_parsers.act_egutegia_parser import ActEgutegiaParser

url = 'http://www.euskolabelliga.com/resultados/index.php?id=eu'
file = urllib.request.urlopen(url)
content = file.read()
parser = ActEgutegiaParser()
result = parser.parse(content)
print(result)
