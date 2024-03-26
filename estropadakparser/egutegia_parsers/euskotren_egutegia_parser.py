import lxml.html
from ..estropada.estropada import Estropada
from .act_egutegia_parser import ActEgutegiaParser


class EuskotrenEgutegiaParser(ActEgutegiaParser):
    '''Base class to parse the Euskotren calendar'''

    def __init__(self):
        self.document = ''
        self.estropada = None
        self.base_url = 'http://www.euskotrenliga.com'
        self.liga = 'EUSKOTREN'
