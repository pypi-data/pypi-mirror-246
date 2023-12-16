"""
uvicorn examples.async:application
"""

from sys import path as python_path

import logging
import os

from asgiref.wsgi import WsgiToAsgi

EXAMPLES_PATH = os.path.dirname(__file__)
python_path.insert(0, os.path.abspath(
    os.path.join(EXAMPLES_PATH, os.path.pardir)))

# pylint: disable=import-error, wrong-import-position
from poorwsgi import Application  # noqa
from poorwsgi.response import JSONResponse  # noqa

LOGGER = logging.getLogger()
LOGGER.setLevel("FATAL")

app = Application("test")
application = WsgiToAsgi(app)


@app.route("/abc/test")
async def static(req):
    """static url"""
    return "Hello world!"


@app.route("/<backend:word>/<uri:word>")
async def handler(req, backend, uri):
    """Dynamic url"""
    return JSONResponse(backend=backend, uri=uri)
