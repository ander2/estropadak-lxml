# coding=utf-8
import datetime
import json
import sys


class Encoder(json.JSONEncoder):

    def default(self, o):
        return dict(izena=o.__izena, data=o.__data, liga=o.__liga,
                    urla=o.__urla, lekua=o.__lekua, sailkapena=o.__sailkapena)


class Estropada(object):
    """Base class to store a boat race info and result"""

    def __init__(self, izena, **kwargs):
        self.__izena = izena
        self.__kategoriak = []
        self.__puntuagarria = True
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])
        self.version = sys.version_info[1]

    def __gt__(self, other):
        return self.__data > other.__data

    def __lt__(self, other):
        return self.__data < other.__data

    def __repr__(self):
        data = datetime.datetime.fromisoformat(self.__data)
        return '{} ({})'.format(self.izena, data.strftime('%Y-%m-%d %H:%M'))

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
        self.__sailkapena = []
        for taldea in sailkapena:
            if not isinstance(taldea, TaldeEmaitza):
                izena = taldea.pop('talde_izena')
                emaitza = TaldeEmaitza(izena, **taldea)
                self.__sailkapena.append(emaitza)
            else:
                self.__sailkapena.append(taldea)

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

    @property
    def kategoriak(self):
        return self.__kategoriak

    @kategoriak.setter
    def kategoriak(self, data):
        self.__kategoriak = data

    @property
    def puntuagarria(self):
        return self.__puntuagarria

    @puntuagarria.setter
    def puntuagarria(self, data):
        self.__puntuagarria = data

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
                         ensure_ascii=False, indent=4))

    def get_json(self):
        return json.dumps(self, default=self.format_for_json,
                          ensure_ascii=False, cls=Encoder, indent=4)

    def format_for_json(self, o):
        attrs = ['id', 'izena', 'data', 'liga', 'urla', 'lekua', 'oharrak', 'kategoriak', 'puntuagarria']
        obj = {}
        for at in attrs:
            if hasattr(o, at):
                obj[at] = getattr(o, at)
        if hasattr(o, 'sailkapena'):
            obj['sailkapena'] = [sailk.format_for_json(sailk) for sailk in sorted(o.sailkapena)]
        return obj


class TaldeEmaitza(object):
    ''' Base class to store a team's result in a race pass '''

    def __init__(self, talde_izena, **kwargs):
        self.talde_izena = talde_izena
        self.ziabogak = []
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.postua = ''

    @property
    def ziabogak(self):
        return self.__ziabogak

    @ziabogak.setter
    def ziabogak(self, ziabogak):
        self.__ziabogak = ziabogak

    @property
    def kalea(self):
        try:
            return self.__kalea
        except AttributeError:
            return None

    @kalea.setter
    def kalea(self, kalea):
        self.__kalea = kalea

    @property
    def tanda(self):
        try:
            return self.__tanda
        except AttributeError:
            return None

    @tanda.setter
    def tanda(self, tanda):
        self.__tanda = tanda

    @property
    def tanda_postua(self):
        try:
            return self.__tanda_postua
        except AttributeError:
            return None

    @tanda_postua.setter
    def tanda_postua(self, tanda_postua):
        self.__tanda_postua = tanda_postua

    @property
    def denbora(self):
        try:
            return self.__denbora
        except AttributeError:
            return None

    @denbora.setter
    def denbora(self, denbora):
        self.__denbora = denbora

    @property
    def posizioa(self):
        try:
            return self.__posizioa
        except AttributeError:
            return None

    @posizioa.setter
    def posizioa(self, posizioa):
        self.__posizioa = posizioa

    @property
    def puntuazioa(self):
        try:
            return self.__puntuazioa
        except AttributeError:
            return None

    @puntuazioa.setter
    def puntuazioa(self, puntuazioa):
        self.__puntuazioa = puntuazioa

    @property
    def kategoria(self):
        try:
            return self.__kategoria
        except AttributeError:
            return None

    @kategoria.setter
    def kategoria(self, kategoria):
        self.__kategoria = kategoria

    def ziaboga_gehitu(self, ziaboga):
        self.ziabogak.append(ziaboga)

    def __repr__(self):
        formatua = ''
        args = []
        if getattr(self, 'posizioa'):
            formatua = formatua + '[{:2}]'
            args.append(getattr(self, 'posizioa'))

        for t in ['tanda', 'kalea', 'tanda_postua']:
            if getattr(self, t):
                formatua = formatua + '{:1}'
                args.append(getattr(self, t))

        formatua = formatua + '{:30}'
        args.append(getattr(self, 'talde_izena'))

        if getattr(self, 'ziabogak'):
            formatua = formatua + '{:25}'
            args.append(' '.join(self.ziabogak))

        if getattr(self, 'denbora'):
            formatua = formatua + '{:8}'
            args.append(getattr(self, 'denbora'))

        return formatua.format(*args)

    def __gt__(self, other):
        if self.posizioa is None:
            return True
        elif other.posizioa is None:
            return False
        else:
            return self.posizioa > other.posizioa

    def __lt__(self, other):
        if self.posizioa is None:
            return False
        elif other.posizioa is None:
            return True
        else:
            return self.posizioa < other.posizioa

    def format_for_json(self, tanda):
        tanda_obj = {
            "talde_izena": self.talde_izena,
            "kalea": self.kalea,
            "tanda": self.tanda,
            "tanda_postua": self.tanda_postua,
            "ziabogak": self.ziabogak,
            "denbora": self.denbora,
            "posizioa": self.posizioa,
            "puntuazioa": self.puntuazioa,
        }
        if hasattr(self, 'kategoria') and self.kategoria:
            tanda_obj['kategoria'] = self.kategoria
        return tanda_obj
