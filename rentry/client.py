import http.cookiejar
import urllib.parse
import urllib.request
from http.cookies import SimpleCookie
from json import loads as json_loads
import os
from dotenv import load_dotenv, dotenv_values

# Load environment variables
load_dotenv()
env = dotenv_values()

# Default values if not in env
if 'BASE_PROTOCOL' not in env:
    env['BASE_PROTOCOL'] = 'https://'
if 'BASE_URL' not in env:
    env['BASE_URL'] = 'rentry.co'

_headers = {"Referer": f"{env['BASE_PROTOCOL']}{env['BASE_URL']}"}


class RentryClient:
    """Client for interacting with Rentry.co API."""

    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        urllib.request.install_opener(self.opener)
        self._csrftoken = None
        self._get_csrf_token()

    def _get_csrf_token(self):
        """Get CSRF token from rentry.co"""
        cookie = SimpleCookie()
        cookie.load(vars(self.get(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}"))['headers']['Set-Cookie'])
        self._csrftoken = cookie['csrftoken'].value
        return self._csrftoken

    def get(self, url, headers={}):
        """Make GET request"""
        merged_headers = _headers.copy()
        merged_headers.update(headers)
        request = urllib.request.Request(url, headers=merged_headers)
        return self._request(request)

    def post(self, url, data=None, headers={}):
        """Make POST request"""
        merged_headers = _headers.copy()
        merged_headers.update(headers)
        postdata = urllib.parse.urlencode(data).encode() if data else None
        request = urllib.request.Request(url, postdata, headers=merged_headers)
        return self._request(request)

    def _request(self, request):
        """Process request and return response"""
        response = self.opener.open(request)
        response.status_code = response.getcode()
        response.data = response.read().decode('utf-8')
        return response

    def new(self, text, url='', edit_code='', metadata=''):
        """Create a new entry"""
        payload = {
            'csrfmiddlewaretoken': self._csrftoken,
            'text': text
        }
        if url:
            payload['url'] = url
        if edit_code:
            payload['edit_code'] = edit_code
        if metadata:
            payload['metadata'] = metadata

        return json_loads(self.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}/api/new", payload).data)

    def edit(self, url, edit_code, text, metadata='', update_mode=''):
        """Edit an existing entry"""
        payload = {
            'csrfmiddlewaretoken': self._csrftoken,
            'edit_code': edit_code,
            'text': text
        }
        if metadata:
            payload['metadata'] = metadata
        if update_mode:
            payload['update_mode'] = update_mode

        return json_loads(self.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}/api/edit/{url}", payload).data)

    def raw(self, url, auth_header=None):
        """Get raw markdown text of an existing entry"""
        headers = {}
        if auth_header:
            headers['rentry-auth'] = auth_header

        return json_loads(self.get(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}/api/raw/{url}", headers).data)

    def fetch(self, url, edit_code):
        """Fetch entry details"""
        payload = {
            'csrfmiddlewaretoken': self._csrftoken,
            'edit_code': edit_code
        }
        return json_loads(self.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}/api/fetch/{url}", payload).data)

    def delete(self, url, edit_code):
        """Delete an entry"""
        payload = {
            'csrfmiddlewaretoken': self._csrftoken,
            'edit_code': edit_code
        }
        return json_loads(self.post(f"{env['BASE_PROTOCOL']}{env['BASE_URL']}/api/delete/{url}", payload).data)


# Helper functions for simpler API access
def new(text, url='', edit_code='', metadata=''):
    """Create a new entry"""
    client = RentryClient()
    return client.new(text, url, edit_code, metadata)

def edit(url, edit_code, text, metadata='', update_mode=''):
    """Edit an existing entry"""
    client = RentryClient()
    return client.edit(url, edit_code, text, metadata, update_mode)

def raw(url, auth_header=None):
    """Get raw markdown text of an existing entry"""
    client = RentryClient()
    return client.raw(url, auth_header)

def fetch(url, edit_code):
    """Fetch entry details"""
    client = RentryClient()
    return client.fetch(url, edit_code)

def delete(url, edit_code):
    """Delete an entry"""
    client = RentryClient()
    return client.delete(url, edit_code)
