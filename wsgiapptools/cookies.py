from Cookie import SimpleCookie


ENVIRON_KEY = 'wsgiapptools.cookies'


def set_cookie(environ, cookie):
    """
    Set a cookie using the Cookies in the WSGI environ.
    """
    return get_cookies(environ).set_cookie(cookie)


def delete_cookie(environ, cookie_name):
    """
    Delete a cookie using the Cookies in the WSGI environ.
    """
    return get_cookies(environ).delete_cookie(cookie_name)


def get_cookies(environ):
    """
    Find the Cookies instance from the WSGI environ.
    """
    return environ[ENVIRON_KEY]


class Cookies(object):
    """
    Cookie manager, associated with a WSGI environ.
    """

    def __init__(self, environ):
        self.environ = environ
        self.headers = []

    def set_cookie(self, cookie):
        """
        Set a cookie.

        The cookie will actually be recorded in the WSGI environ and the
        'Set-Cookie' header will be generated with the responses are first
        sent.

        'cookie' can be one of four things:

            * a string: the value is considered a cookie header value, i.e. the
              bit that would normally be added after 'Set-Cookie: '.
            * (name, value) tuple: a persistent cookie is created.
            * (name, None) tuple: the named cookie will be removed.
            * cookie instance: e.g. one of the cookie types in Python's Cookie
              module.
        """
        if isinstance(cookie, str):
            pass
        elif isinstance(cookie, tuple):
            name, value = cookie
            cookie = SimpleCookie()
            cookie[name] = value or ''
            cookie[name]['path'] = self.environ['SCRIPT_NAME'] or '/'
            if value is None:
                cookie[name]['expires'] = 0
                cookie[name]['max-age'] = 0
            cookie = cookie.output(header='').strip()
        else:
            cookie = cookie.output(header='').strip()
        self.headers.append(cookie)

    def delete_cookie(self, cookie_name):
        """
        Delete the named cookie.
        """
        self.set_cookie((cookie_name, None))


def cookies_middleware_factory(app):
    """
    Create a cookie middleware WSGI application around the given WSGI
    application.
    """
    def middleware(environ, start_response):
        def _start_response(status, response_headers, exc_info=None):
            # Extend the headers with cookie setting headers.
            cutter = environ[ENVIRON_KEY]
            response_headers.extend(('Set-Cookie', header) for header in cutter.headers)
            # Call wrapped app's start_response.
            return start_response(status, response_headers, exc_info)
        environ[ENVIRON_KEY] = Cookies(environ)
        return app(environ, _start_response)
    return middleware

