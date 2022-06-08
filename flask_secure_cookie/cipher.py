# -*- coding: utf-8 -*-
import base64
import binascii
import os

from cryptography.hazmat.primitives.ciphers import aead

from flask_secure_cookie.utils import b64encode_and_unicode
from flask_secure_cookie.utils import to_bytes
from flask_secure_cookie.utils import to_unicode


class CipherError(Exception):
    pass


class AESGCMCipher(object):
    """A wrapper class for encryption/decryption.

    This class uses AES_GCM cipher to encrypt/decrypt strings.
    """

    def __init__(self, secret_keys: str, delimiter: str = ';'):
        ciphers = []
        for secret_key in secret_keys.split(delimiter):
            secret_key = secret_key.strip()
            ciphers.append(aead.AESGCM(to_bytes(secret_key)))
        self._ciphers = ciphers

    def encrypt(self, data: str, associated_data: str = '',
                nonce: str = None) -> str:
        if nonce is None:
            nonce = os.urandom(12)

        try:
            iv = to_bytes(nonce)
            v = self._ciphers[0].encrypt(
                nonce=iv,
                data=to_bytes(data),
                associated_data=to_bytes(associated_data))
            ct = binascii.hexlify(iv) + b':' + binascii.hexlify(v)
            return b64encode_and_unicode(ct)
        except Exception:
            raise CipherError

    def decrypt(self, data: str, associated_data: str = '') -> str:
        try:
            ct = base64.b64decode(to_bytes(data))
            pos = ct.find(b':')
            iv = binascii.unhexlify(ct[:pos])
            v = binascii.unhexlify(ct[pos + 1:])

            for cipher in self._ciphers:
                try:
                    txt = cipher.decrypt(
                        nonce=iv,
                        data=v,
                        associated_data=to_bytes(associated_data))
                    return to_unicode(txt)
                except Exception:
                    pass
        except Exception:
            raise CipherError
