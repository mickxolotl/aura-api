# -*- coding: utf-8 -*-
import json
import logging

import requests

logger = logging.getLogger('aura')


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


def json_iter_parse(response_text):
    decoder = json.JSONDecoder(strict=False, object_hook=Dummy)
    idx = 0
    while idx < len(response_text):
        obj, idx = decoder.raw_decode(response_text, idx)
        yield obj
