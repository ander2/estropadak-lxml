# coding=utf-8
import lxml.html
import re
import logging
import datetime
import urllib.request
import sys
from estropadakparser.parsers.parser import Parser
from estropadakparser.parsers.actparser import ActParser
from estropadakparser.parsers.arcparser import ArcParser
from estropadakparser.parsers.euskotrenparser import EuskotrenParser
from estropadakparser.parsers.arc_legacy_parser import ArcParserLegacy
from estropadakparser.parsers.eteparser import EteParser

from estropadakparser.estropada.estropada import Estropada, TaldeEmaitza


class EstropadakParser(object):
    '''Factory class that returns the right parser
    based on the league name '''
    parsers = {
        'act': ActParser,
        'arc': ArcParser,
        'euskotren': EuskotrenParser,
        'arc-legacy': ArcParserLegacy,
        'ete': EteParser
    }

    def __new__(cls, league):
        try:
            return cls.parsers[league]()
        except KeyError:
            raise RuntimeError('Not registered parser. Available parsers: act, arc1, arc2, ete, euskotren')
        

    @classmethod
    def register(cls, league, parser):
        cls.parsers[league] = parser


if __name__ == "__main__":
    p = None
    liga = sys.argv[1].lower()
    modua = sys.argv[2].lower()
    try:
        liga_kod = liga 
        if (liga == 'arc1' or liga == 'arc2'):
            liga_kod = 'arc'
        p = EstropadakParser(liga_kod)
        estropada = p.parse(*sys.argv[3:])
        if (modua == 'json'):
            print(estropada.dump_json())
        else:
            print(estropada.dump_text())
    except KeyError:
        raise RuntimeError('Not registered parser. Available parsers: act, arc1, arc2, ete, euskotren')
    