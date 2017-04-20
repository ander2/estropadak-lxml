import urllib.request
from estropadakparser.estropadakparser import ActEgutegiaParser

url = 'http://www.euskolabelliga.com/resultados/index.php?id=eu'
file = urllib.request.urlopen(url)
content = file.read()
parser = ActEgutegiaParser()
result = parser.parse(content)
print(result)
