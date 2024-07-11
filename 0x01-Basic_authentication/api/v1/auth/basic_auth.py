#!/usr/bin/env python3

"""
Authenticates user information
"""

from typing import TypeVar, Tuple
from base64 import b64decode, decode
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """
    Extends Auth class
    """

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """Returns the decoded value of a Base64 string
        """
        if auth_header is None or not isinstance(auth_header, str):
            return None
        if 'Basic ' not in auth_header:
            return None
        return auth_header[6:]

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """ Returns the Base64 part of the Authorization header
        """
        if b64_auth_header is None or not isinstance(b64_auth_header, str):
            return None
        try:
            b64 = base64.b64decode(b64_auth_header)
            b64_decode = b64.decode('utf-8')
        except Exception:
            return None
        return b64_decode

    def extract_user_credentials(
            self, decoded_b64_auth_header: str) -> (str, str):
        """ Returns the user email and password from the Base64 decoded value
        """
        if decoded_b64_auth_header is None or not isinstance(
            decoded_b64_auth_header, str)\
                or ':' not in decoded_b64_auth_header:
            return (None, None)
        return decoded_b64_auth_header.split(':', 1)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password.
        """
        if user_email is None or not isinstance(
                user_email, str) or user_pwd is None or not isinstance(
                user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)

        if not auth_header:
            return None

        extract_base64 = self.extract_base64_authorization_header(auth_header)
        decode_base64 = self.decode_base64_authorization_header(extract_base64)
        user_credentials = self.extract_user_credentials(decode_base64)
        user_email = user_credentials[0]
        user_password = user_credentials[1]

        user_credentials = self.user_object_from_credentials(
            user_email, user_password)

        return user_credentials
