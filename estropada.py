# coding=utf-8
import sys
import json


class Encoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__


class Estropada(object):
    ''' Base class to store a boat race info and result '''

    def __init__(self, izena, estropada_id):
        self.__taldeak = []
        self.__izena = izena
        self.__data = ''
        self.__lekua = ''
        self.__urla = ''
        self.__estropada_id = estropada_id
        self.__oharrak = ''
        self.version = sys.version_info[1]

    @property
    def izena(self):
        return self.__izena

    @izena.setter
    def izena(self, izena):
        self.__izena = izena

    @property
    def taldeak(self):
        return self.__taldeak

    def taldeak_add(self, taldea):
        self.__taldeak.append(taldea)

    @property
    def oharrak(self):
        return self.__oharrak

    @oharrak.setter
    def oharrak(self, oharra):
        self.__oharrak = oharra

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def lekua(self):
        return self.__lekua

    @lekua.setter
    def lekua(self, data):
        self.__lekua = data

    @property
    def urla(self):
        return self.__urla

    @urla.setter
    def urla(self, data):
        self.__urla = data

    def dump_text(self):
        print self.__izena
        print '{0:^6}\t{1:^5}\t{2:^5}\t{3:^30}\t{4:^25}\t{5:^8}'.format(
              'Postua', 'Tanda', 'Kalea', 'Taldea', 'Ziabogak', 'Denbora')
        for talde in sorted(self.__taldeak, key=lambda x: x.posizioa):
            print u'{0:<6}\t{1:^5}\t{2:^5}\t{3:<30}\t{4:<25}\t{5:<8}'.format(
                  str(talde.posizioa), talde.tanda, talde.kalea,
                  talde.talde_izena, u'\t'.join(talde.ziabogak),
                  talde.denbora)

    def dump_json(self):
        print json.dumps(self, default=self.format_for_json,
                         cls=Encoder, indent=4)

    def format_for_json(self, o):
        if isinstance(o, Estropada):
            return dict(izena=o.__izena, sailkapena=o.__taldeak)
        else:
            return o.__dict__


class TaldeEmaitza(object):
    ''' Base class to store a team's result in a race pass '''

    def __init__(self, talde_izena, **kwargs):
        self.talde_izena = talde_izena
        self.talde_id = ''
        self.ziabogak = []
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        self.postua = ''

    def ziaboga_gehitu(self, ziaboga):
        self.ziabogak.append(ziaboga)
