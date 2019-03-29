# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('aura')


class Colors:
    COLORS = {
        0: 'white',
        1: 'black',
        2: 'yellow',
        3: 'red',
        19: 'blue gradient',
        20: 'green gradient',
        46: 'purple gradient',
    }

    WHITE = 0
    BLACK = 1
    YELLOW = 2
    RED = 3
    BLUE_GRADIENT = 19
    GREEN_GRADIENT = 20
    PURPLE_GRADIENT = 46


class Dummy:
    def __init__(self, dictionary=None):
        if dictionary is None:
            dictionary = {}
        elif not isinstance(dictionary, dict):
            raise TypeError('dictionary should be dict')

        self.__dict__['_dict'] = dictionary

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getattr__(self, item):
        return self._dict[item]

    def __setattr__(self, key, value):
        self._dict[key] = value

    def get(self, item, default=None):
        return self._dict.get(item, default)

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return repr(self._dict)

    def __contains__(self, item):
        return item in self._dict

    @property
    def as_dict(self):
        return self._dict
