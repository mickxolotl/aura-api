# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('aura')


class BasicConfig:
    USER_AGENT = 'Mozilla/5.0 (Linux; Android 8.1.0; Aura Phone; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36 YandexSearch/8.05 YandexSearchBrowser/8.05'
    DEFAULT_APP_VERSION = '3.27.2'

    HTTP_TIMEOUT = 10  # лимит ожидания ответа
    API_DELAY = .3  # задержка между повторными запросами
    HTTP_METHOD_CORRECTION = True
    # при ошибке Invalid action пробовать с альтернативным HTTP методом,
    # за исключением случаев, когда метод указан вручную


config = BasicConfig

def configure(**kwargs):
    fields = [x for x in config.__dict__.keys() if not x.startswith('__')]
    for k, v in kwargs.items():
        if k not in fields:
            raise KeyError('%s does not contain %s' % (config.__name__, k))
        setattr(config, k, v)
