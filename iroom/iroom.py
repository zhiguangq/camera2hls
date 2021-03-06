#!/usr/bin/env python
import os
import time
import re
import hashlib
from flask import Flask
from flask import request
import platform

def checkIsGetLiveStream(name):
        try:
                with open(name, 'r') as f:
                        lines = f.readlines()
                        f.close()
                        for line in lines:
                                if re.search('time',line):
                                        return 1
        except IOError:
                return -1
        return -1

app = Flask(__name__)

@app.route('/api/stoplivestream', methods=["GET", 'POST'])
def stoplivestreamHandler():
    if platform.system() == "Linux":
        os.system('./stop.py ' + request.args.get("ip") + ' ' +  request.args.get("port") + ' ' + request.args.get("name") + ' &')
    else:
        print request.args
    return "OK"

@app.route('/api/getlivestream', methods=["GET", 'POST'])
def getlivestreamHandler():
    if platform.system() == "Linux":
        os.system('./start.py ' + request.args.get("ip") + ' ' + request.args.get("port") + ' ' + request.args.get( "name") + ' ' + request.args.get("livelimit") + ' &')
    else:
        print request.args
    time.sleep(1)
    counts=25
    ret="NO"
    while counts>0:
        rets = checkIsGetLiveStream(request.args.get( "name") + '.log')
        if rets > 0:
            ret="YES"
            break
        else:
            ret="NO"
        counts = counts - 1
        time.sleep(0.2)
    # TODO
    return "{\"Url\":\"http://106.14.62.202/live/" + request.args.get("ip") + "_" +  request.args.get("port") + "_" + request.args.get("name") + ".m3u8\",\"Ret\":\"" + ret + "\"}"

@app.route('/api/getvodstream', methods=["GET", 'POST'])
def getvodstreamHandler():
    if platform.system() == "Linux":
        #find the input H.264 file
	#outputfile = hashlib.md5(os.path.basename(request.args.get("filepath")))
	#outputfile = hashlib.md5(request.args.get("filepath"))
	#print outputfile.hexdigest()
        if os.path.exists(request.args.get("filepath")):
        	#os.system('./vod.sh ' + request.args.get("filepath") + ' '+outputfile.hexdigest())
        	os.system('./vod.sh ' + request.args.get("filepath") + ' '+os.path.basename(request.args.get("filepath")))
	else:
		print "Can not find : " + request.args.get("filepath")
    else:
        print request.args
    #return "{\"Url\":\"http://106.14.62.202/live/" + outputfile.hexdigest() + ".m3u8\"}"
    return "{\"Url\":\"http://106.14.62.202/live/" + os.path.basename(request.args.get("filepath")) + ".m3u8\"}"

@app.route('/')
def hello_world():
    return 'Hello Flask!'


@app.route('/favicon.ico')
def favicon():
    return 'Favicon'


if __name__ == '__main__':
    print 'Begin...'
    app.run(host='0.0.0.0', port=808)
