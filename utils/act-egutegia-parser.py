import urllib.request
import requests
from estropadakparser.egutegia_parsers.act_egutegia_parser import ActEgutegiaParser
from estropadakparser.parsers.actparser import ActParser
import os

API_URL = os.environ['API_URL']
API_USER = os.environ['API_USER']
API_PASS = os.environ['API_PASSWORD']
credentials = {
    'username': API_USER,
    'password': API_PASS
}
r = requests.post(f'{API_URL}/auth', json=credentials)
token = r.json()['access_token']

url = 'http://www.euskolabelliga.com/resultados/index.php?id=eu'
file = urllib.request.urlopen(url)
content = file.read()
parser = ActEgutegiaParser()
estropadak = parser.parse(content)

for estropada in estropadak:
    print(estropada.izena)

for estropada in estropadak:
    act_parser = ActParser()
    estropada_full = act_parser.parse(estropada.urla)
    estropada.data = estropada_full.data
    payload = estropada.get_json()
    r = requests.post(
        f"{API_URL}/estropadak",
        data=payload,
        headers={
            'Authorization': f'JWT {token}',
            'Content-Type': 'application/json'
        })
    print(f'{r.status_code}\t{r.text}')
