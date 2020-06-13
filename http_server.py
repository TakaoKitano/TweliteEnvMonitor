#!/usr/bin/env python3
from wsgiref import simple_server, util
 
import sys
import os
import json
import mimetypes

import appenv
 
filenames = { 
    "index.html": appenv.APP_ROOT + "index.html",
    "master.json": appenv.FILENAME_MASTER,
    "channels.json": appenv.AMBIENT_CHANNELS
}

requests = {
        "request?cmd=reboot": "reboot",
        "request?cmd=shutdown": "shutdown",
        "request?cmd=upgrade": "upgrad"
}


def app(environ, respond):
    print("request_uri=", util.request_uri(environ))

    if util.request_uri(environ).endswith("/request?cmd=reboot"):
        print("### reboot")
        os.system("sudo reboot")
    if util.request_uri(environ).endswith("/request?cmd=shutdown"):
        print("### shutdown")
        os.system("sudo shutdown -h now")
    if util.request_uri(environ).endswith("/request?cmd=upgrade"):
        print("### upgrade")
        os.system("git pull origin master")
        os.system("cd config && git pull origin master && cd ..")

    name = environ['PATH_INFO'][1:]
    if name in filenames:
        fn = filenames[name]
    else:
        fn = filenames["index.html"]
    type = mimetypes.guess_type(fn)[0]
    if os.path.exists(fn):
        respond('200 OK', [('Content-Type', type)])
        return util.FileWrapper(open(fn, "rb"))
    else:
        respond('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'not found']

if __name__ == '__main__':
    with simple_server.make_server('', 3000, app) as httpd:
        print("Serving on port 3000...")
        httpd.serve_forever()
