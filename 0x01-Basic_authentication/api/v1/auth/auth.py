#!/usr/bin/env python3

"""
Template for authentication system
"""

from flask import request
from typing import List, TypeVar


class Auth():
    """
    Authentification methods
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        # Add slash to all cases for consistency
        if path[-1] != '/':
            path += '/'
        if excluded_paths[-1] != '/':
            excluded_paths += '/'

        astericks = [stars[:-1]
                     for stars in excluded_paths if stars[-1] == '*']

        for stars in astericks:
            if path.startswith(stars):
                return False

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Flask request object
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Flask request object
        """
        return None
