# coding=utf-8
import sys
import json


class Encoder(json.JSONEncoder):

    def default(self, o):
        return dict(izena=o.__izena, data=o.__data, liga=o.__liga,
                    urla=o.__urla, lekua=o.__lekua, sailkapena=o.__sailkapena)


class Estropada(object):
    """Base class to store a boat race info and result"""

    def __init__(self, izena, **kwargs):
        self.__izena = izena
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
        self.version = sys.version_info[1]

    def __gt__(self, other):
        return self.__data > other.__data

    def __lt__(self, other):
        return self.__data < other.__data

    def __repr__(self):
        return '{} ({})'.format(self.izena, self.__data)

    @property
    def izena(self):
        return self.__izena

    @izena.setter
    def izena(self, izena):
        self.__izena = izena

    @property
    def sailkapena(self):
        return self.__sailkapena

    @sailkapena.setter
    def sailkapena(self, sailkapena):
        self.__sailkapena = sailkapena

    def taldeak_add(self, taldea):
        if not hasattr(self, 'sailkapena'):
            self.sailkapena = []
        self.__sailkapena.append(taldea)

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
    def data(self, mydata):
        self.__data = mydata

    @property
    def liga(self):
        return self.__liga

    @liga.setter
    def liga(self, liga):
        self.__liga = liga

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
        print(self.__izena)
        print('{0:^6}\t{1:^5}\t{2:^5}\t{3:^30}\t{4:^25}\t{5:^8}'.format(
              'Postua', 'Tanda', 'Kalea', 'Taldea', 'Ziabogak', 'Denbora'))
        for talde in sorted(self.__sailkapena, key=lambda x: x.posizioa):
            print(u'{0:<6}\t{1:^5}\t{2:^5}\t{3:<30}\t{4:<25}\t{5:<8}'.format(
                  str(talde.posizioa), talde.tanda, talde.kalea,
                  talde.talde_izena, u'\t'.join(talde.ziabogak),
                  talde.denbora))

    def dump_json(self):
        print(json.dumps(self, default=self.format_for_json,
                         cls=Encoder, indent=4))

    def get_json(self):
        return json.dumps(self, default=self.format_for_json,
                          cls=Encoder, indent=4)

    def format_for_json(self, o):
        attrs = ['izena', 'data', 'liga', 'urla', 'lekua', 'oharrak']
        obj = {}
        for at in attrs:
            if hasattr(o, at):
                obj[at] = getattr(o, at)
        if hasattr(o, 'sailkapena'):
            obj['sailkapena'] = o.sailkapena
        return obj


class TaldeEmaitza(object):
    ''' Base class to store a team's result in a race pass '''

    def __init__(self, talde_izena, **kwargs):
        self.talde_izena = talde_izena
        self.ziabogak = []
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.postua = ''

    def ziaboga_gehitu(self, ziaboga):
        self.ziabogak.append(ziaboga)

    def __repr__(self):
        # return '[{:2}] {:20} {} '.format(self.posizioa, self.talde_izena)
        return '[{:2}] {:1} {:1} {:1} {:30} {:25} {:8}'.format(
                  self.posizioa, self.tanda, self.kalea, self.tanda_postua,
                  self.talde_izena, ' '.join(self.ziabogak),
                  self.denbora)

    def __gt__(self, other):
        return self.posizioa > other.posizioa

    def __lt__(self, other):
        return self.posizioa < other.posizioa
