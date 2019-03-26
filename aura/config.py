# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('aura')



class BasicConfig:
    USER_AGENT = ''
    DEFAULT_API_VERSION = ''

    HTTP_TIMEOUT = 10  # лимит ожидания ответа
    API_DELAY = .3  # задержка между повторными запросами