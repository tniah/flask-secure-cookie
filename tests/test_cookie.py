# -*- coding: utf-8 -*-
import unittest

from flask import Flask
from flask import jsonify

from flask_secure_cookie import FlaskSecureCookie


class FlaskSecureCookieTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app = Flask(__name__)
        app.config[
            'COOKIE_SECRET_KEYS'
        ] = '4e1TmBkk1Mn0v1jVRsG47EjrqCdLVsFY:wbLwnm9OQyzKi0SK'
        app.config['COOKIE_SECRET_KEYS_DELIMITER'] = ':'
        app.config['COOKIE_ASSOCIATED_DATA'] = 'test'
        app.config['COOKIE_NAME'] = 'authentication_session'
        cookie = FlaskSecureCookie(app)
        self.userinfo = {'name': 'TNiaH', 'email': 'tronghaibk2008@gmail.com'}
        self.client = app.test_client()

        @app.route('/cookie/encrypt')
        def encrypt_cookie():
            resp = jsonify({'success': True})
            resp.status_code = 200
            cookie.save_cookie(resp,
                               key=app.config['COOKIE_NAME'],
                               value=self.userinfo)
            return resp

        @app.route('/cookie/decrypt')
        def decrypt_cookie():
            userinfo = cookie.load_cookie(key=app.config['COOKIE_NAME'])
            resp = jsonify(userinfo)
            resp.status_code = 200
            return resp

    def test_cookie(self):
        resp = self.client.get('/cookie/decrypt', headers={'Cookie': None})
        self.assertEqual(resp.json, '')
        resp = self.client.get('/cookie/encrypt')
        cookie = resp.headers.get('set-cookie')
        resp = self.client.get('/cookie/decrypt', headers={'Cookie': cookie})
        self.assertEqual(resp.json, self.userinfo)
