# coding=utf-8
import lxml.html
import re
import logging
import datetime
import urllib.request
from .parsers.parser import Parser
from .parsers.actparser import ActParser
from .parsers.arcparser import ArcParser
from .parsers.euskotrenparser import EuskotrenParser
from .parsers.arc_legacy_parser import ArcParserLegacy
from .parsers.eteparser import EteParser

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
        return cls.parsers[league]()

    @classmethod
    def register(cls, league, parser):
        cls.parsers[league] = parser
