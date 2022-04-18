import urllib.request
import requests
from estropadakparser.egutegia_parsers.arc_egutegia_parser import ArcEgutegiaParser
from estropadakparser.parsers.arcparser import ArcParser
import os
import sys

if len(sys.argv) < 3:
    print('act-egutegia-parser <urtea> <liga>')
    exit()

urtea = sys.argv[1]
liga = sys.argv[2]

API_URL = os.environ['API_URL']
API_USER = os.environ['API_USER']
API_PASS = os.environ['API_PASSWORD']
credentials = {
    'username': API_USER,
    'password': API_PASS
}
r = requests.post(f'{API_URL}/auth', json=credentials)
token = r.json()['access_token']

url = 'http://www.liga-arc.com/es/calendario/' + urtea
file = urllib.request.urlopen(url)
content = file.read()
parser = ArcEgutegiaParser(liga.upper())
estropadak = parser.parse(content)

for estropada in estropadak:
    print(estropada.izena)

for estropada in estropadak:
    act_parser = ArcParser()
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
    print(f'{r.status_code}\t{estropada.izena}')
