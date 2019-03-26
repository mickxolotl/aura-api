# -*- coding: utf-8 -*-
import logging
import requests
import json

from .config import config
from .exceptions import AuraAPIError, AuraAuthError
from .utils import json_iter_parse

logger = logging.getLogger('aura')


class Session:
    API_URL = 'https://yandex.ru/aura/api/'

    def __init__(self):
        self._session = requests.Session()
        self._session.headers['Accept'] = 'application/json, text/plain, */*'
        self._session.headers['User-Agent'] = config.USER_AGENT
        self._session.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self._session.headers['X-Requested-With'] = 'ru.yandex.searchplugin'

        self.usable = False  # остается задать Session_id и yandexuid куки

    def update_csrf(self):
        resp = self._session.get(self.API_URL + 'user/status/')
        resp_json = resp.json()
        if not resp_json['status']:
            raise AuraAPIError(resp_json)

        if 'X-Csrf-Token' not in resp.headers:
            raise AuraAuthError('Error recieveing csrf token')

        self._session.headers['x-csrf-token'] = resp.headers.get('X-Csrf-Token')
        self.usable = True

    def make_request(self, method, data):
        print('%s %s%s %s' % (method.suggested_http_method, self.API_URL, method, data))
        if method.api.app_version:
            params = {'appVersion': method.api.app_version}
        else:
            params = {}

        if method.suggested_http_method == 'GET':
            params.update(data)
            body = None
        else:
            body = json.dumps(data)

        _resp = self._session.request(method.suggested_http_method, self.API_URL + method.method_name,
                                      params=params, json=body, timeout=config.HTTP_TIMEOUT)

        resp = next(json_iter_parse(_resp.text))
        if resp.code == 200:
            return resp.data
        else:
            raise AuraAPIError(resp)


class AuthSession(Session):
    """
    Сессия, имитирующая авторизацию по логину-паролю
    """
    def __init__(self, login, password):
        super(AuthSession, self).__init__()
        self.login = login
        self.password = password


class CookieSession(Session):
    """
    Сессия, использующая Session_id и yandexuid куки вместо авторизации по логину-паролю
    """
    def __init__(self, session_id, yandexuid):
        super(CookieSession, self).__init__()
        self._session.cookies.update({'Session_id': session_id, 'yandexuid': yandexuid})

        self.update_csrf()

