#!/usr/bin/env python

#
# Accept an image URL as an HTTP GET
# Create a thumbnail of that image
# Write JPEG data back to the client
#
# $Id: thumbnailer.py,v 1.7 2016/10/15 12:51:06 mgoddard Exp mgoddard $
#

import base64
import os, sys
from PIL import Image
from flask import (Flask, request, g, send_from_directory, send_file)
import urllib
import cStringIO # With the 'c'
import StringIO  # Without the 'c'
import re

app = Flask(__name__)
port = int(os.getenv("PORT", 18080))
thumbSize = 256, 256

def getFileExt(url):
    rv = None
    m = re.match('^.+\.([^.]+)$', url)
    if m:
        rv = m.group(1)
    return rv

def getFileName(url):
    rv = None
    m = re.match('^.+/(.+?)\.[A-Za-z]{3,4}$', url)
    if m:
        rv = m.group(1)
    return rv

"""
 Example: http://localhost:18080/?size=256&urlBase64=aHR0cDoL3...QmlcGc=
 If the requested size exceeds the size of the image, the original size is used
 
 Ref. http://pillow.readthedocs.io/en/3.1.x/reference/Image.html
"""
@app.route('/', methods = ['POST', 'GET'])
def thumb():
    size = request.args.get('size')
    if size is None:
        size = thumbSize
    else:
        size = int(size), int(size)
    urlBase64 = request.args.get('urlBase64')
    url = base64.b64decode(urlBase64)
    print "Processing URL \"%s\" now ..." % url
    file = cStringIO.StringIO(urllib.urlopen(url).read())
    img = Image.open(file)
    img.thumbnail(size)
    img_io = StringIO.StringIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
