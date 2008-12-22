"""
"Flash" messaging support.

A "flash" message is a message displayed on a web page that is removed next
request.
"""

__all__ = ['add_message', 'get_messages', 'flash_middleware_factory']


import itertools
from wsgiapptools import cookies


ENVIRON_KEY = 'wsgiapptools.flash'
COOKIE_NAME = 'flash'


def add_message(request, message, type=None):
    """
    Add a new flash message.

    Note: this can be called multiple times to set multiple messages. The
    messages can be retrieved, using get_messages below, and will be returned
    in the order they were added.
    """
    if type is None:
        type = ''
    flash = '%s:%s' % (type, message)
    request.environ.setdefault(ENVIRON_KEY, []).append(flash)


def get_messages(request):
    """
    Retrieve flash messages found in the request's cookies, returning them as a
    list of (type, message) tuples and deleting the cookies.
    """
    messages = []
    cookie_cutter = cookies.get_cookie_cutter(request.environ)
    for i in itertools.count():
        cookie_name = '%s.%d'%(COOKIE_NAME, i)
        # Try to find the next message. Leave the loop if it does not exist.
        message = request.cookies.get(cookie_name)
        if message is None:
            break
        # Remove the cookie, presumably it will be displayed shortly.
        cookie_cutter.delete_cookie(cookie_name)
        # Parse  and yield the message.
        type, message = message.split(':', 1)
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
            cookie_cutter = cookies.get_cookie_cutter(environ)
            for i, flash in enumerate(environ.get(ENVIRON_KEY, [])):
                cookie_cutter.set_cookie(('%s.%d'%(COOKIE_NAME,i), flash))
            # Call wrapped app's start_response.
            return start_response(status, response_headers, exc_info)
        return app(environ, _start_response)
    return middleware

