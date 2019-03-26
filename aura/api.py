# -*- coding: utf-8 -*-
import time
import requests
import threading
import json
import logging

from .config import config

logger = logging.getLogger('aura')

POST_KEYWORDS = ['edit']


class API:
    def __init__(self, session, app_version=config.DEFAULT_APP_VERSION):
        self.session = session
        self.app_version = app_version
        self.threading_lock = threading.Lock()
        self.delay = config.API_DELAY
        self.last_request = 0

    def __getattr__(self, method_name):
        return Method(self, method_name)

    def __call__(self, method_name, http_method='GET', **method_kwargs):
        return getattr(self, method_name, http_method)(**method_kwargs)


class Method:
    def __init__(self, api, method_name, suggested_http_method='GET'):
        self.method_name = method_name + '/'
        self.api = api
        self.suggested_http_method = suggested_http_method

    def __getattr__(self, method_name):
        suggested_http_method = 'POST' if method_name in POST_KEYWORDS else self.suggested_http_method
        return Method(self.api, self.method_name + method_name, suggested_http_method)

    def __getitem__(self, variable):
        return Method(self.api, self.method_name + variable, self.suggested_http_method)

    def __call__(self, **kwargs):
        with self.api.threading_lock:
            time.sleep(max(0, self.api.last_request + self.api.delay - time.time()))
            resp = self.api.session.make_request(self, kwargs)
            self.api.last_request = time.time()

        return resp

    def __str__(self):
        return self.method_name
