#!/usr/bin/python3
#
# pubambient.py: read current.json and publish to ambient server
# it is supposed to be called every one minute or so
#

import os,sys
import json
import requests
import time
import ambient
from datetime import datetime
from datetime import timedelta
import appenv

#
# load channel data
#
def get_channels():
    filepath = appenv.AMBIENT_CHANNELS
    channels = []
    with  open(filepath, "r") as file:
        channels = json.load(file)
    return channels

#
# construct data to be upload for the specified channel 
#
def construct_upload_data(master, channel):
    now = datetime.now()
    upload = {'created': now.strftime('%Y-%m-%d %H:%M:%S')}
    for key in channel['data'].keys():
        nodename = channel['data'][key]["node"]
        typename = channel['data'][key]["type"]
        if nodename in master:
            upload[key] = master[nodename][typename]
    return upload

#
# upload to cloud
#
def upload(channel, data):
    am = ambient.Ambient(channel['channelid'], channel['writekey'])
    am.send(data)

def main():
    with  open(appenv.FILENAME_MASTER, "r") as file:
        master = json.load(file)
        print(master)  

        channels = get_channels()
        for channel in channels:
            data = construct_upload_data(master, channel)
            print(channel["title"], data)
            upload(channel, data)
            time.sleep(2)

if __name__ == '__main__':
    main()
