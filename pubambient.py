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
        for channel in channels:
            print("channelid={}".format(channel['channelid']))  
            print("writekey={}".format(channel['writekey']))  
            print("labels={}".format(channel['labels']))  
    return channels

#
# construct data to be upload for the specified channel 
#
def construct_upload_data(master, channel):
    now = datetime.now()
    upload = {'created': now.strftime('%Y-%m-%d %H:%M:%S')}
    for nodename in master:
        labels = channel['labels']
        if nodename+'_temperature' in labels:
            node = master[nodename]
            key_temperature = labels[nodename+'_temperature']
            key_humidity = labels[nodename+'_humidity']
            #
            # check if datetime is up to date
            #
            minutes_ago = now - timedelta(minutes=5)
            dt = datetime.strptime(node['datetime'], '%Y-%m-%d %H:%M:%S')
            if dt > minutes_ago:
                upload[key_temperature] = node['temperature']
                upload[key_humidity] = node['humidity']
            else:
                print(nodename, 'is not working since ', node['datetime'])
    return upload

def upload(channel, data):
    print("sending...", data)
    am = ambient.Ambient(channel['channelid'], channel['writekey'])
    am.send(data)

def main():
    with  open(appenv.FILENAME_MASTER, "r") as file:
        master = json.load(file)
        print(master)  

        channels = get_channels()
        for channel in channels:
            data = construct_upload_data(master, channel)
            upload(channel, data)
            time.sleep(5)


if __name__ == '__main__':
    main()
