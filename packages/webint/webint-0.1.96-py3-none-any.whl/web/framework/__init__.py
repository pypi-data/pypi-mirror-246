"""
A web application framework.

Strongly influenced by [Aaron Swartz][0]' "anti-framework" `web.py` this
library aims to cleanly abstract low-level web functionality through
a Pythonic API.

> Think about the ideal way to write a web app.
>   Write the code to make it happen.

                           ~ Aaron Swartz [1]

[0]: http://aaronsw.com
[1]: https://webpy.org/philosophy

"""

from __future__ import annotations

import asyncio
import collections
import getpass
import hashlib
import inspect
import mimetypes
import os
import pathlib
import platform
import re
import secrets
import shutil
import signal
import sys
import time
import urllib
import warnings  # mf2py's beautifulsoup's unspecified parser -- force lxml?
from base64 import b64decode, b64encode
from time import sleep

import Crypto.Random.random
import gevent.pywsgi
import gunicorn.app.base
import pendulum
import pkg_resources
import sqlyte

# import errno
import toml
import unidecode
import watchdog.events
import watchdog.observers
import webagt
from rich.console import Console

from newmath import nb60_re, nbdecode, nbencode, nbrandom

from .. import templating
from ..dt import now, parse_dt
from ..response import Status  # noqa
from ..response import (
    OK,
    Accepted,
    BadRequest,
    Conflict,
    Created,
    Forbidden,
    Found,
    Gone,
    MethodNotAllowed,
    MovedPermanently,
    MultiStatus,
    NoContent,
    NotFound,
    PermanentRedirect,
    SeeOther,
    Subscription,
    Unauthorized,
)
from ..util import dump, load
from .letsencrypt import generate_cert
from .passphrases import generate_passphrase, verify_passphrase
from .util import add_rel_links, header, json, shift_headings, tx

console = Console()
mimetypes.init()
mimetypes.add_type("application/wheel+zip", ".whl")

warnings.simplefilter("ignore")

random = secrets.SystemRandom()

__all__ = [
    "application",
    "load_mounts",
    "serve",
    "anti_csrf",
    "form",
    "best_match",
    "require_auth",
    "tx",
    "header",
    "add_rel_links",
    "Application",
    "Resource",
    "nbencode",
    "nbdecode",
    "nbrandom",
    "templates",
    "generate_cert",
    "now",
    "dump",
    "load",
    "default_session_timeout",
    "textslug",
    "get_host_hash",
    "b64encode",
    "b64decode",
    "timeslug",
    "enqueue",
    "get_apps",
    "get_sites",
    "nb60_re",
    "generate_passphrase",
    "verify_passphrase",
    "sleep",
    "random",
    "resume_session",
    "StandaloneServer",
    "parse_dt",
]

sessions_model = sqlyte.model(
    "WebSessions",
    sessions={
        "timestamp": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
        "identifier": "TEXT NOT NULL UNIQUE",
        "data": "TEXT NOT NULL",
    },
)
templates = templating.templates(__name__)
methods = [
    "head",
    "get",
    "post",
    "put",
    "delete",
    "options",
    "patch",
    "propfind",
    "report",
]
applications = {}
default_session_timeout = 86400


def ismethod(obj):
    """"""
    return (
        inspect.ismethod(obj)
        and obj.__name__.isupper()
        and obj.__name__.lower() in methods
    )


def application(
    name,
    _prefix="",
    prefix="",
    model=None,
    db=True,
    static=None,  # XXX in favor of explicit mount
    icon=None,  # XXX in favor of explicit mount
    mounts=None,
    automount=False,
    autotemplate=False,
    wrappers=None,
    sessions=False,  # XXX in favor of explicitly wrapper
    host=None,
    port=False,
    args=None,
) -> Application:
    if name in applications:  # TODO FIXME XXX remove concept of multi-module singleton?
        app = applications[name]
        # XXX app.prefix = prefix  # FIXME does this have a side effect?
        if wrappers:
            app.add_wrappers(wrappers)
        if args:
            app.add_path_args(**args)
        # TODO add models?
    else:
        app = Application(
            name,
            db=db,
            model=model,
            host=host,
            static=static,
            icon=icon,
            sessions=sessions,
            port=port,
            mounts=mounts,
            automount=automount,
            autotemplate=autotemplate,
            wrappers=wrappers,
            args=args,
        )
        app.reload_config()
        app._prefix = _prefix
        app.prefix = prefix
        applications[name] = app
    return app


def load_mounts():
    try:
        saved_mounts = load(path="mounts.json")
    except FileNotFoundError:
        saved_mounts = []
        for apps in get_apps().values():
            app_name, app, package_name, (app_obj,) = apps[0]
            saved_mounts.append([package_name, app_name])
        dump(saved_mounts, path="mounts.json")
    mounts = []
    for package_name, app_name in saved_mounts:
        for apps in get_apps().values():
            app = apps[0]
            if app[2] == package_name and app[0] == app_name:
                mounts.append(app[1])
    return mounts


def get_env():
    return


def get_host_hash(path):
    return hashlib.sha256(str(path.resolve()).encode("utf-8")).hexdigest()[:6]


def setup_servers(root, app, bot):
    """Initialize and configure servers (web, nginx, redis, supervisor)."""
    root = pathlib.Path(root).resolve()
    root_hash = get_host_hash(root)
    env = pathlib.Path(os.getenv("VIRTUAL_ENV"))
    root.mkdir()
    (root / "etc").mkdir()

    with (root / "etc/redis.conf").open("w") as fp:
        fp.write(str(templates.redis(root)))
    with (root / "etc/supervisor.conf").open("w") as fp:
        fp.write(
            str(templates.supervisor(root, root_hash, getpass.getuser(), env, app, bot))
        )
    with (root / "etc/nginx.conf").open("w") as fp:
        fp.write(str(templates.nginx(root_hash)))

    (root / "run").mkdir(parents=True)
    with (root / "etc/tor_stem_password").open("w") as fp:
        fp.write(str(random.getrandbits(100)))

    session_salt = Crypto.Random.random.randint(10**63, 10**64)
    cfg = {
        "root": str(root),
        "watch": str(env / "src"),
        "session": {"salt": str(session_salt)},
    }
    with (root / "etc/web.conf").open("w") as fp:
        json.dump(cfg, fp, indent=4, sort_keys=True)
    return root


class StandaloneServer(gunicorn.app.base.BaseApplication):
    """A standalone gunicorn webapp context for the canopy."""

    def __init__(self, app, port):
        """Initialize standalone server."""
        self.options = {"bind": f"localhost:{port}", "workers": 2}
        self.application = app
        super().__init__()

    def load_config(self):
        """Load configuration values."""
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """Load the application."""
        return self.application


async def serve(wsgi_app, port=9300, socket=None, workers=2, watch_dir="."):
    if socket:
        binding = f"unix:{socket}"
    else:
        binding = f"0.0.0.0:{port}"

    SYSTEM = platform.system()
    if SYSTEM == "Windows":
        command = ["waitress-serve", "--listen", binding, wsgi_app]
    else:
        command = [
            "gunicorn",
            wsgi_app,
            "--bind",
            binding,
            "--worker-class",
            "gevent",
            "--workers",
            str(workers),
        ]

    async def output_filter(input_stream, output_stream):
        while not input_stream.at_eof():
            output = await input_stream.readline()
            if not output.startswith(b"filtered"):
                output_stream.buffer.write(output)
                output_stream.flush()

    class Watchdog(watchdog.events.FileSystemEventHandler):
        """Restart server when source directory changes."""

        def on_modified(self, event):
            if event.src_path.endswith((".py", ".toml")):
                # while reload_lock:
                #     time.sleep(1)
                if SYSTEM == "Windows":
                    proc.send_signal(signal.SIGTERM)
                else:
                    proc.send_signal(signal.SIGHUP)

    proc = None
    event_handler = Watchdog()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)
    observer.start()
    try:
        while True:
            proc = await asyncio.create_subprocess_exec(
                *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await asyncio.gather(
                output_filter(proc.stderr, sys.stderr),
                output_filter(proc.stdout, sys.stdout),
            )
            await proc.wait()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    if SYSTEM == "Windows":
        proc.send_signal(signal.SIGTERM)
    else:
        proc.send_signal(signal.SIGQUIT)


def get_sites():
    """"""
    apps = collections.defaultdict(list)
    for ep in pkg_resources.iter_entry_points("websites"):
        try:
            handler = ep.load()
        except (FileNotFoundError, ModuleNotFoundError):
            print(f"couldn't load entry point: {ep}")
            continue
        try:
            raw_meta = ep.dist.get_metadata("PKG-INFO")
        except FileNotFoundError:
            raw_meta = ep.dist.get_metadata("METADATA").partition("\n\n")[0]
        ep.dist.metadata = dict(
            line.partition(": ")[0::2] for line in raw_meta.splitlines()
        )
        apps[ep.dist].append((ep.name, handler, ep.module_name, ep.attrs))
    return apps


def get_apps():
    """"""
    apps = collections.defaultdict(list)
    for ep in pkg_resources.iter_entry_points("webapps"):
        try:
            handler = ep.load()
        except (FileNotFoundError, ModuleNotFoundError):
            print(f"couldn't load entry point: {ep}")
            continue
        try:
            raw_meta = ep.dist.get_metadata("PKG-INFO")
        except FileNotFoundError:
            raw_meta = ep.dist.get_metadata("METADATA").partition("\n\n")[0]
        ep.dist.metadata = dict(
            line.partition(": ")[0::2] for line in raw_meta.splitlines()
        )
        apps[ep.dist].append((ep.name, handler, ep.module_name, ep.attrs))
    return apps


def get_app(object_reference):
    """"""
    for ep in pkg_resources.iter_entry_points("webapps"):
        if f"{ep.module_name}:{ep.attrs[0]}" == object_reference:
            return ep.name, ep.handler


def best_match(handlers, *args, **kwargs):
    """"""
    handler_types = [handler for handler, _ in handlers.items()]
    best_match = tx.request.headers.accept.best_match(handler_types)
    tx.response.headers.content_type = best_match
    return dict(handlers)[best_match](*args, **kwargs)


_punct_re = r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+'
_punct_split = re.compile(_punct_re).split


def textslug(title, delim="_", lower=True):
    """
    return a path slug containing a normalized version of `title`

    Defaults to delimiting words by "_" and enforcing all lowercase.
    Also makes intelligent path-friendly replacements (e.g. "&" to "and").

        >>> textslug("Surfing with @Alice & @Bob!")
        'surfing_with_alice_and_bob'

    """
    # TODO use formal normalization tooling:

    #   import unicodedata
    #   normalized = unicodedata.normalize("NFKC", title)

    #   title.encode("punycode")

    #   from confusable_homoglyphs import confusables
    #   bool(confusables.is_dangerous(title))

    result = []
    if lower:
        title = title.lower()
    title = title.replace(" & ", " and ")
    for word in _punct_split(title):
        result.extend(unidecode.unidecode(word).split())
    slug = delim.join(result)
    slug = slug.replace(":", "")  # XXX REMOVE WHEN MENTIONS REMOVED KV
    return slug


def timeslug(dt):
    """
    return a path slug containing date and time

    Date is encoded in standard YYYY/MM/DD form while the time is encoded
    as the NewBase60 equivalent of the day's centiseconds.

    """
    return f"{dt.year}/{dt.format('MM')}/{dt.format('DD')}"


def anti_csrf(handler):
    """"""
    # TODO csrf-ify forms with class name "x-secure"
    yield


class Form(dict):
    def __init__(self, *requireds, **defaults):
        _data = tx.request.body._data
        for required in requireds:
            if required not in _data:
                err_msg = "required `{}` not present in request"
                raise BadRequest(err_msg.format(required))
        super(Form, self).__init__(defaults)
        if isinstance(_data, str):
            return  # TODO FIXME what to do here? fix for Jupyter
        for key in _data.keys():
            if isinstance(_data[key], list):
                items = []
                for item in _data[key]:
                    if getattr(item, "filename", False):
                        items.append(File(item.filename, item))
                    else:
                        items.append(item.value)
                self[key] = items
            else:
                if key == "file" or getattr(_data[key], "filename", False):
                    value = File(key, _data[key])
                else:
                    try:
                        value = _data.getfirst(key)
                    except AttributeError:
                        value = _data[key]
                if isinstance(defaults.get(key), list):
                    value = [value]
                self[key] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        self[name] = value


form = Form


class File:

    """"""

    def __init__(self, name, fileobj):
        self.name = name
        self.fileobj = fileobj

    def save(self, filepath=None, file_dir=None, overwrite=False, **options):
        """"""
        if filepath is None:
            filepath = self.fileobj.filename
        filepath = pathlib.Path(filepath)
        if file_dir:
            file_dir = pathlib.Path(file_dir)
            file_dir.mkdir(exist_ok=True)
            filepath = file_dir / filepath
        # TODO handle required
        required = options.pop("required", False)
        if required:
            requireds = [required]
            if required == "jpg":
                requireds.append("jpeg")
            if not self.fileobj.filename.lower().endswith(tuple(requireds)):
                raise BadRequest("`{}` not `{}`".format(self.name, required))
        # self._ensure_dir_exists(dirpath)
        self.fileobj.file.seek(0)
        # while True:
        #     sugar = nbrandom(2)
        #     path = dirpath / self.name
        #     path = path.parent / "{}-{}{}".format(path.stem, sugar,
        #                                           path.suffix)
        if required:
            suffix = "." + required
        else:
            suffix = pathlib.Path(self.fileobj.filename).suffix
        filepath = filepath.with_suffix(suffix)
        if filepath.exists() and overwrite is False:
            raise FileExistsError("{} already exists".format(filepath))
        with filepath.open("wb") as fp:
            shutil.copyfileobj(self.fileobj.file, fp)
        return filepath

    # def _ensure_dir_exists(self, dirpath):
    #     try:
    #         os.makedirs(str(dirpath))
    #     except OSError as exc:
    #         if exc.errno == errno.EEXIST and dirpath.is_dir():
    #             pass
    #         else:
    #             raise


class Resource:

    """ """

    def __init__(self, **kwargs):
        self.__dict__ = dict(kwargs)
        self._args = kwargs
        # XXX self._resources = ResourceData()
        # XXX for resource_name, value in kwargs.items():
        # XXX     table, _, column = resource_name.partition("_")
        # XXX     self._resources[table][column] = value

    def get_data(self):
        try:
            data = self.__dict__.pop("data")
        except KeyError:
            try:
                loader = self.load
            except AttributeError:

                def loader():
                    pass

            data = loader()
        self.data = data

    def delegate(self, handler, *args, shift_headings=1, **kwargs):
        # TODO uhhmmm...
        kwargs.update(shift_headings=shift_headings)
        return handler()._get(self, *args, **kwargs)

    @classmethod
    def _get(cls, parent, **kwargs):
        """"""
        header_shift = kwargs.pop("shift_headings", None)
        if "_data" in parent.__dict__:
            parent._data.update(kwargs.get("data", {}))
        parent.__dict__.pop("data", None)  # NOTE magic name "data" is reserved
        kwargs.update(parent.__dict__)
        try:
            handler = cls(**kwargs)
            handler.get_data()
            content = handler.get()
        except NotFound:
            return "not found"
        if header_shift:
            try:
                content._body = shift_headings(str(content), header_shift)
            except AttributeError:
                pass
        return content

    # XXX def __getattr__(self, name):
    # XXX     pass  # TODO FIXME shuts up the linter on `self.{path_template}`

    def __contains__(self, item):
        return item in dir(self)


# XXX class ResourceData(collections.OrderedDict):
# XXX
# XXX     def __missing__(self, key):
# XXX         self[key] = collections.OrderedDict()
# XXX         return self[key]


class Response:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body[0].decode()
        self.parsed = None

    @property
    def dom(self):
        if self.parsed is None:
            self.parsed = webagt.parse(self.body)
        return self.parsed


class Application:
    """
    A web application.

        >>> app = Application("example")
        >>> @app.wrap
        ... def contextualize(handler, app):
        ...     yield
        >>> @app.control(r"")
        ... class Greeting:
        ...     def get(self):
        ...         return "hello world"

    # TODO >>> response = app.get(r"")
    # TODO >>> response[0]
    # TODO '200 OK'
    # TODO >>> response[2][0]
    # TODO b'hello world'

    """

    def __init__(
        self,
        name,
        db=True,
        args=None,
        model=None,
        static=None,
        icon=None,
        sessions=False,
        mounts=None,
        automount=False,
        autotemplate=False,
        wrappers=None,
        host=None,
        port=False,
    ):
        self.name = name
        self.wrappers = []
        self.pre_wrappers = []
        self.post_wrappers = []
        self.host = host
        self.port = port
        self.path_args = {}
        if args:
            self.add_path_args(**args)
        self.mounts = []
        if automount:
            mounts = load_mounts()
        self.controllers = []  # TODO use ordered dict
        self.after_controllers = []  # TODO use ordered dict
        self.unprefixed_controllers = []

        if model:
            self._model = sqlyte.model(name, **model)
            self.query = self._model.control

        if mounts:
            self.mount(*mounts)

            def set_data_sources(handler, app):
                # tx.host.kv = kv.db(tx.request.uri.host, ":", {"jobs": "list"})
                # cache_db = sqlyte.db(f"cache-{tx.request.uri.host}.db", cache.model)
                # tx.host.cache = cache(db=cache_db)
                tx.host.db = sqlyte.db("site.db", *models)
                # tx.host.db = sqlyte.db(f"site-{tx.request.uri.host}.db", *models)
                yield

            self.wrappers.insert(0, resume_session)  # 2nd position
            self.wrappers.insert(0, set_data_sources)  # 1st position
            models = [sessions_model] + [
                app._model for _, app in self.mounts if getattr(app, "_model", None)
            ]
            if model:
                models.append(self._model)
            # XXX for site_db in pathlib.Path().glob("site-*.db"):
            # XXX     sqlyte.db(site_db, *models)
        if wrappers:
            self.add_wrappers(*wrappers)
        # for _, mounted_app in self.mounts:
        #     self.add_wrappers(*mounted_app.wrappers)
        #     mounted_app.wrappers = []

        self.view = None
        self.autotemplate = autotemplate
        if self.autotemplate:
            try:
                self.view = templating.TemplatePackage("templates")
            except (AttributeError, ModuleNotFoundError):
                pass
        if not self.view:
            try:
                self.view = templating.templates(name)
            except ModuleNotFoundError:
                pass

        self.static_path = pathlib.Path("static")
        if not self.static_path.exists():
            try:
                self.static_path = pathlib.Path(
                    pkg_resources.resource_filename(name, "static")
                )
            except ModuleNotFoundError:
                self.static_path = None

        # for method in http.spec.request.methods[:5]:
        #     setattr(self, method, functools.partial(self.get_handler,
        #                                             method=method))
        # XXX try:
        # XXX     self.view = templating.templates(name, tx=tx)
        # XXX except ImportError:
        # XXX     try:
        # XXX         self.view = templating.templates(name + ".__web__", tx=tx)
        # XXX     except ImportError:
        # XXX         pass
        if port:
            self.serve(port)

    @property
    def model(self):
        if self._model:
            return self._model(tx.db)

    def serve(self, port, host="127.0.0.1"):
        # must be called from custom jupyter kernel/head of your program:
        # XXX from gevent import monkey
        # XXX monkey.patch_all()
        def write(logline):
            _, _, _, _, _, method, path, _, status, _, duration = logline.split()
            method = method.lstrip('"')
            duration = round(float(duration) * 1000)
            print(
                f"<div class=httplog>"
                f"<span>{self.host}</span>"
                f"<span>{method}</span>"
                f"<span>{path}</span>"
                f"<span>{status}</span>"
                f"<span>{duration}<span>ms</span></span>"
                f"</div>"
            )

        class Log:
            pass

        Log.write = write

        server = gevent.pywsgi.WSGIServer((host, port), self, log=Log)
        # self.server.serve_forever()
        self.server = gevent.spawn(server.serve_forever)
        self.server.spawn()  # TODO start()?

    def reload_config(self, path="webcfg.ini"):
        self.cfg = {}
        path = os.getenv("WEBCFG", path)
        try:
            with pathlib.Path(path).open() as fp:
                self.cfg = toml.load(fp)
        except (FileNotFoundError, TypeError):
            pass
        return path

    def update_config(self, key, value):
        path = self.reload_config()
        self.cfg[key] = value
        with pathlib.Path(path).open("w") as fp:
            toml.dump(self.cfg, fp)

    def add_wrappers(self, *wrappers):
        self.wrappers.extend(wrappers)

    # XXX def add_controller(self, *wrappers):
    # XXX     self.wrappers.extend(wrappers)

    def add_path_args(self, **path_args):
        self.path_args.update(
            {k: v.replace(r"\!", nb60_re) for k, v in path_args.items()}
        )

    def wrap(self, handler, when=None):
        """
        decorate a generator to run at various stages during the request

        """
        if when == "pre":
            self.pre_wrappers.append(handler)
        elif when == "post":
            self.post_wrappers.append(handler)
        else:
            self.wrappers.append(handler)
        return handler
        # def register(controller):
        #     path = path_template.format(**{k: "(?P<{}>{})".format(k, v) for
        #                                    k, v in self.path_args.items()})
        #     self.controllers.append((path, controller))
        #     return controller
        # return register

    # @property
    # def resource(self):
    #     class Resource(type):
    #         def __new__(cls, name, bases, attrs):
    #             resource = type(name, bases, attrs)
    #           path = attrs["path"].format(**{k: "(?P<{}>{})".format(k, v) for
    #                                          k, v in self.path_args.items()})
    #             self.controllers.append((path, resourcer))
    #             controller.__web__ = path
    #             return resource
    #     return Resource

    def control(self, path_template=None, try_late=False, prefixed=True):
        """
        decorate a class to run when request path matches template

        """

        def register(controller):
            # TODO allow for reuse of parent_app's path_arg definitions
            # XXX try:
            # XXX     path_args = dict(self.parent_app.path_args,
            #                          **self.path_args)
            # XXX except AttributeError:
            # XXX     path_args = self.path_args
            arg_templates = {
                k: "(?P<{}>{})".format(k, v) for k, v in self.path_args.items()
            }
            try:
                path = path_template.format(**arg_templates)
            except KeyError as err:
                raise KeyError(
                    "undefined URI fragment" " type `{}`".format(err.args[0])
                )

            # TODO metaclass for `__repr__` -- see `app.controllers`
            class Route(controller, Resource):
                __doc__ = controller.__doc__
                __web__ = path_template, arg_templates, self
                handler = controller

            Route.prefixed = prefixed
            if prefixed:
                try:
                    path = "/".join((self._prefix, path))
                except AttributeError:
                    pass
                if try_late:
                    self.after_controllers.append((path.strip("/"), Route))
                else:
                    self.controllers.append((path.strip("/"), Route))
            else:
                self.unprefixed_controllers.append((path.strip("/"), Route))
            return Route

        return register

    def mount(self, *apps):
        """
        add an `application` to run when request path matches template

        """
        for app in apps:
            app.parent_app = self
            self.add_wrappers(*app.wrappers)  # TODO add pre and post wrappers
            path = app.prefix.format(
                **{k: "(?P<{}>{})".format(k, v) for k, v in self.path_args.items()}
            )
            self.mounts.append((path, app))
            self.unprefixed_controllers.extend(app.unprefixed_controllers)

    def __repr__(self):
        return "<web.application: {}>".format(self.name)

    def get(self, path):
        return self.request("get", path)

    def post(self, path):
        return self.request("post", path)

    def request(self, method, path):
        environ = {
            "HTTP_ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "HTTP_ACCEPT_ENCODING": "gzip, deflate",
            "HTTP_ACCEPT_LANGUAGE": "en-US,en;q=0.5",
            "HTTP_CONNECTION": "keep-alive",
            "HTTP_COOKIE": "",
            "HTTP_DNT": "1",
            "HTTP_HOST": "test",
            "HTTP_UPGRADE_INSECURE_REQUESTS": "1",
            "HTTP_USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
            "PATH_INFO": f"/{path}",
            "QUERY_STRING": "",
            "RAW_URI": "/",
            "REMOTE_ADDR": "127.0.0.1",
            "REMOTE_PORT": "34798",
            "REQUEST_METHOD": method.upper(),
            "SCRIPT_NAME": "",
            "SERVER_NAME": "0.0.0.0",
            "SERVER_PORT": "8081",
            "SERVER_PROTOCOL": "HTTP/1.1",
            "SERVER_SOFTWARE": "gunicorn/20.1.0",
            # "gunicorn.socket": <gevent._socket3.socket at 0x7fc0baaa7040 object, fd=11, family=2, type=1, proto=6>,
            # "wsgi.errors": <gunicorn.http.wsgi.WSGIErrorsWrapper object at 0x7fc0bcbe2910>,
            # "wsgi.file_wrapper": <class 'gunicorn.http.wsgi.FileWrapper'>,
            # "wsgi.input": <gunicorn.http.body.Body object at 0x7fc0ba7a5160>,
            "wsgi.input_terminated": True,
            "wsgi.multiprocess": True,
            "wsgi.multithread": True,
            "wsgi.run_once": False,
            "wsgi.url_scheme": "http",
            "wsgi.version": (1, 0),
        }
        response = {}

        def start_response(status, headers):
            response["status"] = status
            response["headers"] = headers

        response["body"] = self(environ, start_response)
        return Response(**response)

    def __call__(self, environ, start_response):
        """The WSGI callable."""
        start_utc = now()
        start_unix = time.time()
        tx.request._contextualize(environ)
        tx.response._contextualize()
        path = tx.request.uri.path

        if path.startswith("static/") or re.match("[a-f0-9]+.wasm", path):
            if not path.startswith("static/"):
                header("Location", f"/static/{path}")
                start_response("301 Moved Permanently", tx.response.headers.wsgi)
                return [b""]
            asset_path = path.partition("/")[2]

            # TODO # BEGIN NGINX MODE
            # TODO header("X-Accel-Redirect", f"/X/{asset_path}")
            # TODO start_response("200 OK", tx.response.headers.wsgi)
            # TODO return [b""]
            # TODO # END NGINX MODE

            if asset_path.startswith((".", "/")):
                raise BadRequest("bad filename")
            try:
                asset = self.static_path / asset_path
                with asset.open("rb") as fp:
                    content = fp.read()
            except (AttributeError, FileNotFoundError):
                asset = pathlib.Path(__file__).parent / "static" / asset_path
                try:
                    with asset.open("rb") as fp:
                        content = fp.read()
                except FileNotFoundError:
                    raise NotFound("file not found")
            header("Content-Type", mimetypes.guess_type(asset)[0])
            header("Access-Control-Allow-Origin", "*")
            start_response("200 OK", tx.response.headers.wsgi)
            try:
                content = bytes(content, "utf-8")
            except TypeError:
                pass
            return [content]

        try:
            tx.host._contextualize(
                environ,
                self,
                tx.request.headers.host.name,
                tx.request.headers.host.port,
            )
        except AttributeError:
            raise NotFound("no hostname provided")
        tx.user._contextualize(environ)
        tx.log._contextualize()
        tx.response.headers.content_type = "text/plain"
        # XXX tx.app_name = self.name
        response_hooks = []

        def exhaust_hooks():
            for hook in response_hooks:
                try:
                    next(hook)
                except StopIteration:
                    pass
                except Exception:
                    console.print_exception(show_locals=True)
                    raise

        try:
            tx.request.controller = self.get_controller(path)
            tx.response.headers.x_powered_by = "webint"

            for hook in self.pre_wrappers + self.wrappers + self.post_wrappers:
                if not inspect.isgeneratorfunction(hook):
                    msg = "`{}.{}` is not an iterator, give it a yield"
                    modname = getattr(hook, "__module__", "??")
                    raise TypeError(msg.format(modname, hook.__name__))
                _hook = hook(tx.request.controller, self)
                next(_hook)
                response_hooks.append(_hook)

            method = tx.request.method
            tx.response.status = "200 OK"
            if method == "GET":
                forced_method = Form().get("_http_method")
                if forced_method:
                    method = forced_method.upper()
            tx.request.controller.get_data()  # TODO FIXME err?
            body = self.get_handler(tx.request.controller, method)(
                **tx.request.controller._args
            )
            if body is None:
                raise NoContent()
            if isinstance(body, tuple) and isinstance(body[0], dict):
                body = best_match(body[0], *body[1:])

            try:
                header("Content-Type", body.content_type)
            except AttributeError:
                pass

            tx.response.body = body
            # exhaust_hooks()  # TODO see below to pull hook exhaustion out
        except Status as exc:
            tx.response.status = str(exc)  # TODO exc.status
            tx.response.body = exc.body
            if exc.code == 201:
                tx.response.headers.location = exc.location
            elif exc.code in (301, 302, 303, 307, 308):
                redirect_uri = str(tx.response.body)  # XXX remove apply_dns
                if redirect_uri.startswith("/"):  # relative HTTP(S) URL
                    # XXX tx.response.headers.location = urllib.parse.quote(redirect_uri)
                    tx.response.headers.location = redirect_uri
                else:  # anything else (moz-extension, etc..)
                    tx.response.headers.location = redirect_uri
            elif exc.code == 405:
                tx.response.headers.allow = ", ".join(dict(exc.allowed))
        except Exception:
            if os.getenv("PYTEST_CURRENT_TEST"):
                raise
            console.print_exception(show_locals=True)
            tx.response.status = "500 Internal Server Error"
            tx.response.headers.content_type = "text/html"
            if getattr(tx.user, "is_owner", False):
                body = templates.traceback(*sys.exc_info())
            else:
                body = "<small><code>I have been notified.</code></small>"
                # body = templates.traceback(*sys.exc_info())
                # TODO body = self.view.error.internal()
            tx.response.body = body

        if all(
            (
                not isinstance(tx.response.body, pathlib.Path),
                getattr(tx.request, "controller", False),
                isinstance(tx.response.body, templating.templating.TemplateResult),
            )
        ):
            handling_app = tx.request.controller.__web__[2]
            if getattr(handling_app, "parent_app", None):

                def linkify(link):
                    if link.startswith(
                        ("http://", "https://", "mailto:", "tel:", "magnet:", "#")
                    ):
                        return link
                    if tx.request.controller.prefixed:
                        link = f"/{handling_app.prefix}{link}"
                    return link

                dom = webagt.parse(tx.response.body)
                dom.doc.rewrite_links(linkify)
                tx.response.body._body = dom.html
                if "aside" in tx.response.body:
                    aside_dom = webagt.parse(tx.response.body["aside"])
                    aside_dom.doc.rewrite_links(linkify)
                    tx.response.body.aside = aside_dom.html

        chromeless = str(tx.request.headers.get("X-Chromeless", "0")) == "1"
        naked = getattr(tx.response, "naked", False)
        if chromeless:
            body = "<article id=content"
            if "article_classes" in tx.response.body:
                body += f' class="{" ".join(tx.response.body.article_classes)}"'
            body += ">"
            if tx.request.uri.path:
                breadcrumbs = []
                if "breadcrumbs" in tx.response.body:
                    breadcrumbs = list(tx.response.body.breadcrumbs)
                body += str(
                    templates.render_breadcrumbs(breadcrumbs, tx.request.uri.path)
                )
            title = getattr(tx.response.body, "title", None)
            if title:
                body += f"<h1>{title}</h1>"
            body += f"{tx.response.body}</article>"
            body += "<div class=page-related>"
            if "aside" in tx.response.body:
                body += tx.response.body.aside
            body += "</div>"
            tx.response.body = body
        elif tx.response.headers.content_type == "text/html" and not naked:
            if not isinstance(tx.response.body, str):
                try:
                    template = self.view.template
                except AttributeError:
                    template = lambda x: x
                tx.response.body = template(tx.response.body)

        exhaust_hooks()  # here for mandatory wrappers (eg. session handling)
        # try:
        #     # exhaust_hooks()
        #     pass
        # except:
        #     print("BREAK IN THE HOOK")  # TODO provide debug
        #     raise
        try:
            header("Content-Type", tx.response.body.content_type)
        except AttributeError:
            pass

        duration = round(time.time() - start_unix, 3)
        duration_color = None
        if duration < 0.1:
            pass
        elif duration < 0.5:
            duration_color = "yellow"
        else:
            duration_color = "red"
        duration = f"{duration:.3f}"
        if duration_color:
            duration = f"[{duration_color}]{duration}[/{duration_color}]"

        status = tx.response.status.partition(" ")[0]
        status_color = None
        if status.startswith("3"):
            status_color = "cyan"
        elif status.startswith("4"):
            status_color = "magenta"
        elif status.startswith("5"):
            status_color = "red"
        if status_color:
            status = f"[{status_color}]{status}[/{status_color}]"

        method = tx.request.method
        # XXX host = tx.request.uri.host
        resource = tx.request.uri.path
        if "PYTEST_CURRENT_TEST" not in os.environ:
            console.print(
                f"{start_utc.to_datetime_string()} {duration} "
                f"{status} {method: >6} {resource}"
            )
            for k, v in sorted(tx.request.uri.query.items()):
                console.print(f"    {k}: {v[0]}")

        if isinstance(tx.response.body, templating.templating.TemplateResult):
            pass
        elif isinstance(tx.response.body, dict):
            header("Content-Type", "application/json")
        elif isinstance(tx.response.body, pathlib.Path):
            header("Content-Type", mimetypes.guess_type(tx.response.body)[0])
            if "x-forwarded-for" in tx.request.headers:
                header("X-Accel-Redirect", f"/X/{tx.response.body}")

        try:
            start_response(tx.response.status, tx.response.headers.wsgi)
        except OSError:  # websocket connection broken
            # TODO close websocket connection?
            return []

        if naked:  # causes low-level gunicorn error
            return tx.response.body
        elif isinstance(tx.response.body, pathlib.Path):
            if "x-forwarded-for" in tx.request.headers:
                return []
            else:
                with tx.response.body.open("rb") as fp:
                    content = fp.read()
                return [content]
        elif isinstance(tx.response.body, bytes):
            return [tx.response.body]
        elif isinstance(tx.response.body, templating.templating.TemplateResult):
            pass
        elif isinstance(tx.response.body, dict):
            return [bytes(dump(tx.response.body), "utf-8")]

        tx.response.body = str(tx.response.body)
        if tx.response.headers.content_type == "text/html":
            doctype = "<!doctype html>"
            if not tx.response.body.startswith(doctype):
                tx.response.body = doctype + tx.response.body
        return [bytes(tx.response.body, "utf-8")]

    # def __gevent_call__(self, environ, start_response):
    #     """gevent's WSGI callable."""
    #     tx.request._contextualize(environ)
    #     tx.response._contextualize()
    #     path = tx.request.uri.path
    #     controller = self.get_controller(path)
    #     if tx.request.headers.get("Subscribe") == "keep-alive":
    #         handler = controller._subscribe
    #     else:
    #         handler = controller.get
    #     start_response("200 OK", [("Content-Type", "application/json")])
    #     return handler()

    def get_controller(self, path):
        # TODO softcode `static/` reference
        if path.endswith("/") and not path.startswith("static/"):
            raise PermanentRedirect("/" + path.rstrip("/"))

        outer_self = self

        class ResourceNotFound(Resource):
            def get(self):
                raise NotFound("Resource not found")  # TODO XXX
                error = outer_self.view.error
                # TODO recursively ascend app ancestors
                # try:
                #     error = outer_self.parent_app.view.error
                # except AttributeError:
                #     error = outer_self.parent_app.parent_app.view.error
                raise NotFound(error.resource_not_found())

        def get_resource(controllers):
            for pattern, resource in controllers:
                if isinstance(resource, str):
                    mod = __import__(resource.__module__)
                    resource = getattr(mod, resource)
                match = re.match(r"^{}$".format(pattern), urllib.parse.unquote(path))
                if match:
                    unquoted = (
                        {
                            k: urllib.parse.unquote(v)
                            for k, v in match.groupdict().items()
                            if v
                        }
                        if match
                        else {}
                    )
                    return resource(**unquoted)
            return None

        if resource := get_resource(outer_self.controllers):
            return resource
        for mount, app in outer_self.mounts:
            m = re.match(mount, path)
            if m:
                match_end = m.span()[1]
                controller = app.get_controller(path[match_end:].lstrip("/"))
                if controller is None:
                    continue
                for k, v in m.groupdict().items():
                    setattr(controller, k, v)
                return controller
        if resource := get_resource(outer_self.after_controllers):
            return resource
        if resource := get_resource(outer_self.unprefixed_controllers):
            return resource
        return ResourceNotFound()

    def get_handler(self, controller, method="get"):
        method = method.lower()
        try:
            return getattr(controller, method)
        except AttributeError:
            if method == "head":
                try:
                    return getattr(controller, "get")
                except AttributeError:
                    pass
            exc = MethodNotAllowed(f"{method.upper()} not allowed")
            exc.allowed = inspect.getmembers(controller, ismethod)
            raise exc


def resume_session(handler, app):
    """."""
    # TODO monitor expiration (default_session_timeout)
    data = {}
    try:
        identifier = tx.request.headers["cookie"].morsels["session"]
    except KeyError:
        identifier = None
    else:
        try:
            session = tx.db.select(
                "sessions", where="identifier = ?", vals=[identifier]
            )[0]
        except IndexError:
            identifier = None
        else:
            try:
                data = json.loads(session["data"])
            except json.decoder.JSONDecodeError:
                identifier = None
    tx.user.session = data
    yield
    if tx.user.session:
        if identifier is None:
            salt = "abcdefg"  # FIXME
            secret = f"{random.getrandbits(64)}{salt}{time.time()}{tx.user.ip}"
            identifier = hashlib.sha256(secret.encode("utf-8")).hexdigest()
            tx.user.session.update(
                ip=tx.user.ip, ua=str(tx.request.headers["user-agent"])
            )
            # TODO FIXME add Secure for HTTPS sites (eg. canopy)!
            tx.response.headers["set-cookie"] = (
                ("session", identifier),
                ("path", "/"),
                # "Secure",
                "HttpOnly",
            )
        tx.db.replace("sessions", identifier=identifier, data=dump(tx.user.session))
    else:
        tx.response.headers["set-cookie"] = (
            ("session", identifier),
            ("path", "/"),
            ("max-age", 0),
        )


def require_auth(*allowed_roles):
    def decorate(func):
        def handler(*args, **kwargs):
            if tx.user.session["role"] not in allowed_roles + ("owner",):
                raise Unauthorized("no auth to access this resource")
            return func(*args, **kwargs)

        return handler

    return decorate


class Session(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return super(Session, self).__getattr__(name)

    def __setattr__(self, name, value):
        self[name] = value


icons_app = application("Icon", prefix="icons")


@icons_app.wrap
def insert_icon_rels(handler, app):
    # TODO handle `favicon.ico` requests here
    yield
    if (
        tx.response.status == "200 OK"
        and tx.response.headers.content_type == "text/html"
    ):
        doc = webagt.parse(tx.response.body)
        head = doc.select("head")[0]
        head.append("<link rel=icon href=/icon.png>")
        tx.response.body = doc.html


@icons_app.control(r"icon.png")
class Icon:
    """Your site's icon"""

    def get(self):
        # TODO set `icon_path` when you add the `insert_icon_rels` wrapper
        icon_path = None  # XXX pkg_resources.resource_filename(icon, "icon.png")
        payload = pathlib.Path(icon_path)

        header("Content-Type", "image/png")
        try:
            with payload.open("rb") as fp:
                return fp.read()
        except AttributeError:
            return payload


def enqueue(callable, *args, **kwargs):
    """
    append a function call to the end of the job queue

    """
    signature_id = get_job_signature(callable, *args, **kwargs)
    job_id = nbrandom(9)
    tx.db.insert("job_runs", job_id=job_id, job_signature_id=signature_id)
    return job_id


def get_job_signature(callable, *args, **kwargs):
    """
    return a job signature id creating a record if necessary

    """
    _module = callable.__module__
    _object = callable.__name__
    _args = json.dumps(args)
    _kwargs = json.dumps(kwargs)
    arghash = hashlib.sha256((_args + _kwargs).encode("utf-8")).hexdigest()
    try:
        job_signature_id = tx.db.insert(
            "job_signatures",
            module=_module,
            object=_object,
            args=_args,
            kwargs=_kwargs,
            arghash=arghash,
        )
    except tx.db.IntegrityError:
        job_signature_id = tx.db.select(
            "job_signatures",
            what="rowid, *",
            where="module = ? AND object = ? AND arghash = ?",
            vals=[_module, _object, arghash],
        )[0]["rowid"]
    return job_signature_id
