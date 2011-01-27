"""
"Flash" messaging support.

A "flash" message is a message displayed on a web page that is removed next
request.
"""

__all__ = ['add_message', 'get_messages', 'get_flash',
           'flash_middleware_factory']


import itertools
import webob

from wsgiapptools import cookies


ENVIRON_KEY = 'wsgiapptools.flash'
COOKIE_NAME = 'flash'


def add_message(environ, message, type=None):
    """
    Add the flash message to the Flash manager in the WSGI environ."
    """
    return get_flash(environ).add_message(message, type)


def get_messages(environ):
    """
    Get the flasg messages from the Flash manager in the WSGI environ.
    """
    return get_flash(environ).get_messages()


def get_flash(environ):
    """
    Get the flash manager from the environ.
    """
    return environ[ENVIRON_KEY]


class Flash(object):
    """
    Flash message manager, associated with a WSGI environ.
    """

    def __init__(self, environ):
        self.request = webob.Request(environ)
        self.flashes = []

    def add_message(self, message, type=None):
        """
        Add a new flash message.

        Note: this can be called multiple times to set multiple messages. The
        messages can be retrieved, using get_messages below, and will be returned
        in the order they were added.
        """
        if type is None:
            type = ''
        self.flashes.append('%s:%s'% (type, message))

    def get_messages(self):
        """
        Retrieve flash messages found in the request's cookies, returning them as a
        list of (type, message) tuples and deleting the cookies.
        """
        messages = []
        cookies_mgr = cookies.get_cookies(self.request.environ)
        for i in itertools.count():
            cookie_name = '%s.%d'% (COOKIE_NAME, i)
            # Try to find the next message. Leave the loop if it does not exist.
            message = self.request.cookies.get(cookie_name)
            if not message:
                break
            # Remove the cookie, presumably it will be displayed shortly.
            cookies_mgr.delete_cookie(cookie_name)
            # Parse  and yield the message.
            try:
                type, message = message.split(':', 1)
            except ValueError:
                # Skip an unparseable cookie value.
                pass
            else:
                messages.append((type or None, message))
        return messages


def flash_middleware_factory(app):
    """
    Create a flash middleware WSGI application around the given WSGI
    application.
    """
    def middleware(environ, start_response):
        def _start_response(status, response_headers, exc_info=None):
            # Iterate the new flash messages in the WSGI, setting a 'flash'
            # cookie for each one.
            flash = environ[ENVIRON_KEY]
            cookies_mgr = cookies.get_cookies(environ)
            for i, flash in enumerate(flash.flashes):
                cookies_mgr.set_cookie(('%s.%d'% (COOKIE_NAME, i), flash))
            # Call wrapped app's start_response.
            return start_response(status, response_headers, exc_info)
        environ[ENVIRON_KEY] = Flash(environ)
        return app(environ, _start_response)
    return middleware

