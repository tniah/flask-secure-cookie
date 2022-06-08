# -*- coding: utf-8 -*-
import base64


def to_unicode(s, encoding='utf-8'):
    """Convert the string s to unicode if it is of type bytes.
    Returns:
        Unicode string
    """
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        return s.decode(encoding)
    return s


def to_bytes(s):
    """Convert the string s to a unicode encoded byte string.
    Returns:
        The converted byte string
    """
    if isinstance(s, bytes):
        return s
    elif isinstance(s, str):
        return s.encode('utf-8')
    return s


def b64encode_and_unicode(s):
    """Base64-encode the string s and return the result as a string.
    Returns:
        Base64-encoded string converted to unicode
    """
    return to_unicode(base64.b64encode(to_bytes(s)))
