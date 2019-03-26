# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('aura')


class BasicConfig:
    USER_AGENT = 'Mozilla/5.0 (Linux; Android 8.1.0; Aura Phone; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36 YandexSearch/8.05 YandexSearchBrowser/8.05'
    DEFAULT_APP_VERSION = '3.27.2'

    HTTP_TIMEOUT = 10  # лимит ожидания ответа
    API_DELAY = .3  # задержка между повторными запросами


config = BasicConfig

def configure(**kwargs):
    for k, v in kwargs.items():
        setattr(config, k, v)
