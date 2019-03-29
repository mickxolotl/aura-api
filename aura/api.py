# -*- coding: utf-8 -*-
import logging
import threading
import time
import json

from .config import config

logger = logging.getLogger('aura')

POST_KEYWORDS = ['recover_profile', 'delete_profile', 'tutorial', 'feedback', 'upload_ava', 'update_info',
                 'subscribe', 'unsubscribe', 'favorite', 'complain', 'delete_comment', 'delete', 'edit', 'addpost_new',
                 'author_from_feed', 'feed', 'smartmatching_on', 'smartmatching_off', 'smartmatching',
                 'rate_user', 'smartmatching_open', 'upload_attachment', 'settings', 'invite', 'suggest']  # 11500


class API:
    def __init__(self, session, app_version=config.DEFAULT_APP_VERSION):
        self._session = session
        self._app_version = app_version
        self._threading_lock = threading.Lock()
        self._delay = config.API_DELAY
        self._last_request = 0

    def __getattr__(self, method_name):
        suggested_http_method = 'POST' if method_name in POST_KEYWORDS else 'GET'
        return Method(self, method_name, suggested_http_method)

    def __call__(self, method_name, http_method='GET', **method_kwargs):
        return getattr(self, method_name, http_method)(**method_kwargs)


class Method:
    __slots__ = ('_method_name', '_api', '_suggested_http_method')

    def __init__(self, api, method_name, suggested_http_method='GET'):
        self._method_name = method_name + '/'
        self._api = api
        self._suggested_http_method = suggested_http_method

    def __getattr__(self, method_name):
        suggested_http_method = 'POST' if method_name in POST_KEYWORDS else self._suggested_http_method
        return Method(self._api, self._method_name + str(method_name), suggested_http_method)

    def __getitem__(self, variable):
        return Method(self._api, self._method_name + str(variable), self._suggested_http_method)

    def __call__(self, _http_method=None, **kwargs):
        if self._method_name.endswith('getdoc/'):
            return  # IDE вызывает этот метод. не знаю, как иначе предотвратить нежелательные запросы

        if _http_method:
            self._suggested_http_method = _http_method
        elif kwargs:
            self._suggested_http_method = 'GET' if 'page' in kwargs else 'POST'

        for k, v in kwargs.items():
            if isinstance(v, list) or isinstance(v, tuple):
                kwargs[k] = json.dumps(v)

        with self._api._threading_lock:
            time.sleep(max(0, self._api._last_request + self._api._delay - time.time()))
            # ожидание на случай наличия лимитов на обращение к апи

            resp = self._api._session.make_request(self, kwargs, forced_method=_http_method)
            self._api._last_request = time.time()

        return resp

    def __str__(self):
        return self._method_name
