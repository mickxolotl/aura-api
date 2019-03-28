# -*- coding: utf-8 -*-
import logging
import requests
import json

from .config import config
from .exceptions import AuraAPIError, AuraAuthError, AuraException
from .utils import Dummy

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

    def make_request(self, method, data, forced_method=False):
        logger.debug('%s %s%s %s' % (method._suggested_http_method, self.API_URL, method, data))

        if method._api._app_version:
            params = {'appVersion': method._api._app_version}
        else:
            params = {}

        if method._suggested_http_method == 'GET':
            params.update(data)
            body = None
        else:
            body = json.dumps(data)

        _resp = self._session.request(method._suggested_http_method, self.API_URL + method._method_name,
                                      params=params, json=body, timeout=config.HTTP_TIMEOUT)
        resp = _resp.json(object_hook=Dummy)

        if resp.code == 200:
            return resp.get('data', Dummy())

        elif resp.errors == 'CSRF_INVALID':
            logger.debug('Updating CSRF token')
            self.update_csrf()
            return self.make_request(method, data, forced_method)

        elif config.HTTP_METHOD_CORRECTION and resp.errors == 'Invalid action' and not forced_method:
            method._suggested_http_method = 'POST' if method._suggested_http_method == 'GET' else 'GET'
            result = self.make_request(method, data, forced_method=True)
            logger.warning('Invalid HTTP method suggestion for %s. Corrected: %s' %
                           (method._method_name, method._suggested_http_method))
            return result

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

    def get_cookie_session_args(self):
        args = {
            'session_id': self._session.cookies.get('Session_id'),
            'yandexuid': self._session.cookies.get('yandexuid'),
        }

        if not all(args.values()):
            raise AuraAuthError('User is not authorized')

        return args


class CookieSession(Session):
    """
    Сессия, использующая Session_id и yandexuid куки вместо авторизации по логину-паролю
    """
    def __init__(self, session_id, yandexuid):
        super(CookieSession, self).__init__()
        self._session.cookies.update({'Session_id': session_id, 'yandexuid': yandexuid})

        self.update_csrf()

