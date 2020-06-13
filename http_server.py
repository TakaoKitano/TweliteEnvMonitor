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

def app(environ, respond):
    print("request_uri=", util.request_uri(environ))

    if util.request_uri(environ).endswith("/request?cmd=reboot"):
        print("### reboot")
        respond('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
        return [json.dumps({'message':'reboot requested'}).encode("utf-8")]
        os.system("sudo reboot")
    if util.request_uri(environ).endswith("/request?cmd=shutdown"):
        print("### shutdown")
        respond('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
        return [json.dumps({'message':'shutdown requested'}).encode("utf-8")]
        os.system("sudo shutdown -h now")
    if util.request_uri(environ).endswith("/request?cmd=upgrade"):
        print("### upgrade")
        respond('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
        return [json.dumps({'message':'upgrade requested'}).encode("utf-8")]
        os.system("git pull origin master")
        os.system("cd config && git pull origin master && cd ..")
        os.system("sudo reboot")

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
