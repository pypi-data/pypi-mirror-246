"""This is encoding test application for PoorWSGI connector.

This sample testing example is free to use, modify and study under same BSD
licence as PoorWSGI. So enjoy it ;)
"""

from wsgiref.simple_server import make_server
from sys import path as python_path
from zipfile import ZipFile
from io import BytesIO

import os
import logging as log

EXAMPLES_PATH = os.path.dirname(__file__)
python_path.insert(0, os.path.abspath(
    os.path.join(EXAMPLES_PATH, os.path.pardir)))

# pylint: disable=import-error, wrong-import-position
from poorwsgi import Application  # noqa
from poorwsgi.response import Response, GeneratorResponse  # noqa

logger = log.getLogger()
logger.setLevel("DEBUG")
app = application = Application("encoding")
app.debug = True


@app.route('/zip')
def zipfile(req):
    return Response(b"")


@app.route('/gen_zip')
def gen_zip(req):
    raw_data = BytesIO()

    with ZipFile(raw_data, 'w') as zip_file:
        for i in range(10):
            zip_file.writestr(f"range/{i}.txt", f"Textíček {i}")

    def gen():
        raw_data.seek(0)
        out = raw_data.read(10)
        while out:
            yield out
            out = raw_data.read(10)
    return GeneratorResponse(gen(), content_type="application/zip")


if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 8080, app)
    print("Starting to serve on http://127.0.0.1:8080")
    httpd.serve_forever()
