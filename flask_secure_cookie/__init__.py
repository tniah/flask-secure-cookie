# -*- coding: utf-8 -*-
import json

from flask import request

from flask_secure_cookie.cipher import AESGCMCipher
from flask_secure_cookie.cipher import CipherError


class FlaskSecureCookie(object):

    def __init__(self, app=None):
        self._app = None
        self._cipher = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        if 'COOKIE_SECRET_KEYS' not in app.config \
                or not app.config['COOKIE_SECRET_KEYS']:
            raise RuntimeError(
                'Missing "COOKIE_SECRET_KEYS" in the configuration.')

        app.config.setdefault('COOKIE_SECRET_KEYS_DELIMITER', ';')
        app.config.setdefault('COOKIE_ASSOCIATED_DATA', 'secureCookie')
        self._cipher = AESGCMCipher(
            secret_keys=app.config['COOKIE_SECRET_KEYS'],
            delimiter=app.config['COOKIE_SECRET_KEYS_DELIMITER'])
        self._app = app

    def _serialize(self, value):
        """Serialize and encrypt the cookie data."""
        try:
            encrypted_cookie = self._cipher.encrypt(
                data=json.dumps(value),
                associated_data=self._app.config['COOKIE_ASSOCIATED_DATA'])
            return encrypted_cookie
        except CipherError as e:
            raise e

    def _unserialize(self, serialized_string):
        """Decrypt and unserialize the cookie data."""
        try:
            data = self._cipher.decrypt(
                data=serialized_string,
                associated_data=self._app.config['COOKIE_ASSOCIATED_DATA'])
            return json.loads(data)
        except CipherError:
            return ''

    def save_cookie(
            self,
            response,
            key,
            value='',
            max_age=None,
            expires=None,
            path='/',
            domain=None,
            samesite='None'):
        """Save the data securely in a cookie on response object. """
        response.set_cookie(
            key=key,
            value=self._serialize(value=value),
            max_age=max_age,
            expires=expires,
            path=path,
            domain=domain,
            secure=self._app.config['SESSION_COOKIE_SECURE'],
            httponly=self._app.config['SESSION_COOKIE_HTTPONLY'],
            samesite=samesite)

    def load_cookie(self, key):
        """Load the cookie data from a cookie in the request. """
        cookie_string = request.cookies.get(key, None)
        return self._unserialize(serialized_string=cookie_string)
