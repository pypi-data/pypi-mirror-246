"""Framework utilities."""

import cgi
import datetime
import io
import json
import time
import wsgiref.util

import easyuri
import lxml
import lxml.html
import webagt
from gevent import local

from ..headers import Headers

__all__ = ["tx", "header", "shift_headings", "json"]


def shift_headings(html, header_shift=1):
    """ """
    if not html.strip():
        return ""
    dom = lxml.html.fromstring(html)
    for header in dom.cssselect("h1, h2, h3, h4, h5, h6"):
        header.tag = "h{}".format(int(header.tag[1]) + header_shift)
    output = lxml.html.tostring(dom).decode("utf-8")
    if output.startswith("<div>"):
        output = output[5:-6]
    return output


def header(name, value, add=False):
    """"""
    if add:
        if name not in tx.response.headers:
            tx.response.headers[name] = [value]
        else:
            tx.response.headers[name].append(value)
    else:
        tx.response.headers[name] = value


def make_absolute(path):
    return f"{tx.origin}{path}"


def add_rel_links(**rels):
    """"""
    if not tx.response.body:
        return
    try:
        doc = webagt.parse(tx.response.body)
        head = doc.select("head")[0]
    except IndexError:
        pass
    else:
        for rel, value in rels.items():
            if isinstance(value, tuple):
                link = f"<link rel={rel} href={make_absolute(value[0])}"
                if "title" in value[1]:
                    link += f' title="{value[1]["title"]}"'
                if "type" in value[1]:
                    link += f' type="{value[1]["type"]}"'
                # type={value[1]} title=asdasd>"
                head.append(link + ">")
            else:
                head.append(f"<link rel={rel} href={make_absolute(value)}>")
        tx.response.body = doc.html
    for rel, value in rels.items():
        header("Link", f'<{make_absolute(value)}>; rel="{rel}"', add=True)


def append_to_head(html):
    """"""
    if not tx.response.body:
        return
    try:
        doc = webagt.parse(tx.response.body)
        head = doc.select("head")[0]
    except IndexError:
        pass
    else:
        head.append(html)
        tx.response.body = doc.html


class Context(local.local):
    # TODO still needed?

    def __iter__(self):
        return iter(dir(self))

    def pop(self, attr):
        value = getattr(self, attr)
        delattr(self, attr)
        return value

    # def __contains__(self, attr):
    #     print(dir(self))
    #     return attr in dir(self)


class Host(Context):
    def _contextualize(self, environ, app, name, port):
        self.server = environ["SERVER_SOFTWARE"].partition("/")
        self.domain = environ["HTTP_HOST"]  # TODO XXX environ["HTTP_X_DOMAIN"]
        self.app = app
        self.name = name
        self.port = port


class User(Context):
    # TODO cookie/session

    def _contextualize(self, environ):
        address = environ.get(
            "HTTP_X_FORWARDED_FOR",
            environ.get("HTTP_X_REAL_IP", environ["REMOTE_ADDR"]),
        )
        self.ip = address.partition(",")[0]
        self.language = "en-us"
        self.is_verified = False
        if environ.get("X-Verified", None) == "SUCCESS":
            self.is_verified = environ["X-DN"]
        # self.uri = None
        # self.roles = []


class Request(Context):
    def _contextualize(self, environ):
        self.uri = easyuri.parse(wsgiref.util.request_uri(environ, include_query=1))
        self.method = environ.get("REQUEST_METHOD").upper()
        self.headers = Headers()
        for name, value in environ.items():
            if name.startswith("HTTP_"):
                self.headers[name[5:]] = value
        try:
            self.headers["content-type"] = environ["CONTENT_TYPE"]
        except KeyError:
            pass
        try:
            self.headers["content-length"] = environ["CONTENT_LENGTH"]
        except KeyError:
            pass
        if self.method in ("PROPFIND", "REPORT"):  # NOTE for WebDav
            self.body = lxml.etree.fromstring(environ["wsgi.input"].read())
        elif self.method in ("PUT",):
            self.body = environ["wsgi.input"].read()
        else:
            self.body = RequestBody(environ)

    def __getitem__(self, name):
        return self.body[name]  # XXX .value


class RequestBody:
    def __init__(self, environ):
        try:
            raw_data = environ["wsgi.input"].read()
        except KeyError:
            self._data = {}
            return
        try:
            data = raw_data.decode("utf-8")
        except (AttributeError, UnicodeDecodeError):
            data = raw_data
        try:
            data = json.loads(data)
        except (json.decoder.JSONDecodeError, UnicodeDecodeError):
            try:
                environ["wsgi.input"] = io.BytesIO(raw_data)
                data = cgi.FieldStorage(
                    fp=environ["wsgi.input"], environ=environ, keep_blank_values=True
                )
            except TypeError:
                try:
                    data = raw_data.decode("utf-8")
                except AttributeError:
                    data = raw_data
        self._data = data

    def items(self):
        return {k: self[k] for k in self._data.keys()}

    def get(self, name, default=None):
        try:
            return self._data.getfirst(name, default)
        except AttributeError:
            return self._data.get(name, default)

    def get_list(self, name):
        return self._data.getlist(name)

    def __getitem__(self, name):
        try:
            return self._data.getfirst(name)
        except AttributeError:
            return self._data[name]


class Response(Context):
    def _contextualize(self):
        self.headers = Headers()
        self.body = ""
        self.naked = False


class Model(Context):
    def _contextualize(self):
        pass


class Log(Context):
    def _contextualize(self):
        self.messages = []

    def store(self, message):
        self.messages.append("{}:{}".format(time.time(), message))


class Transaction:
    host = Host()
    user = User()
    request = Request()
    response = Response()
    log = Log()
    m = Model()

    @property
    def app(self):
        return self.host.app

    @property
    def origin(self):
        try:
            netloc = self.host.domain
        except KeyError:
            netloc = self.request.uri.netloc
        scheme = self.request.headers.get("X-Scheme", self.request.uri.scheme)
        if scheme:
            return scheme + "://" + netloc
        else:
            return ""

    # @property
    # def owner(self):
    #     return self.request.uri.host

    # XXX @property
    # XXX def is_owner(self):
    # XXX     return self.owner == self.user.session.get("me")

    @property
    def db(self):
        try:
            return self.host.db
        except AttributeError:
            return self.host.app.db

    @property
    def cache(self):
        try:
            return self.host.cache
        except AttributeError:
            return self.host.app.cache

    @property
    def kv(self):
        try:
            return self.host.kv
        except AttributeError:
            return self.host.app.kv

    @property
    def view(self):
        return self.host.view


tx = Transaction()
