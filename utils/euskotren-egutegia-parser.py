import urllib.request
import requests
from estropadakparser.egutegia_parsers.euskotren_egutegia_parser import EuskotrenEgutegiaParser
from estropadakparser.parsers.euskotrenparser import EuskotrenParser
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

url = 'http://www.euskolabelliga.com/femenina/resultados/index.php?id=eu'
file = urllib.request.urlopen(url)
content = file.read()
parser = EuskotrenEgutegiaParser()
estropadak = parser.parse(content)

for estropada in estropadak:
    print(estropada.izena)

for estropada in estropadak:
    act_parser = EuskotrenParser()
    estropada_full = act_parser.parse(estropada.urla)
    estropada.data = estropada_full.data
    estropada.liga = estropada.liga.upper()
    payload = estropada.get_json()
    r = requests.post(
        f"{API_URL}/estropadak",
        data=payload,
        headers={
            'Authorization': f'JWT {token}',
            'Content-Type': 'application/json'
        })
    if r.status_code == 201:
        print(f'{r.status_code}\t{estropada.izena}')
    else:
        print(f'{r.status_code}')
        print(r.text)
        print(estropada.get_json())
        exit()
