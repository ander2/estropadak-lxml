import urllib.request
import requests
from estropadakparser.egutegia_parsers.ete_egutegia_parser import EteEgutegiaParser
from estropadakparser.parsers.eteparser import EteParser
import sys
import os

if len(sys.argv) < 2:
    print('ete-egutegia-parser <urtea>')
    exit()

urtea = sys.argv[1]

API_URL = os.environ['API_URL']
API_USER = os.environ['API_USER']
API_PASS = os.environ['API_PASSWORD']
credentials = {
    'username': API_USER,
    'password': API_PASS
}
r = requests.post(f'{API_URL}/auth', json=credentials)
token = r.json()['access_token']

url = f'http://www.ligaete.com/es/calendario/{urtea}'
file = urllib.request.urlopen(url)
content = file.read()
parser = EteEgutegiaParser()
estropadak = parser.parse(content)

for estropada in estropadak:
    print(estropada.izena)

for estropada in estropadak:
    ete_parser = EteParser()
    estropada_full = ete_parser.parse(estropada.urla)
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
