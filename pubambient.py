#!/usr/bin/python3
#
# pubambient.py: read current.json and publish to ambient server
# it is supposed to be called every one minute or so
#

import os,sys
import json
import requests
import properties
import time
import ambient
from datetime import datetime
from datetime import timedelta

TEMPERATURE_CHANNELID=properties.AmbientKeys['TEMPERATURE_CHANNELID']
TEMPERATURE_WRITEKEY=properties.AmbientKeys['TEMPERATURE_WRITEKEY']
TEMPERATURE_READKEY=properties.AmbientKeys['TEMPERATURE_READKEY']
HUMIDITY_CHANNELID=properties.AmbientKeys['HUMIDITY_CHANNELID']
HUMIDITY_WRITEKEY=properties.AmbientKeys['HUMIDITY_WRITEKEY']
HUMIDITY_READKEY=properties.AmbientKeys['HUMIDITY_READKEY']

Labels = {'51AB':'d1','226F':'d2','512B':'d3'}

def main():
    FILE_PATH = "/var/tmp/master.json"
    with  open(FILE_PATH, "r") as file:
        master = json.load(file)
        print(master)  

        now = datetime.now()

        temperatures = {'created': now.strftime('%Y-%m-%d %H:%M:%S')}
        humidities = {'created':  now.strftime('%Y-%m-%d %H:%M:%S')}
        for nodename in master:
            if nodename in Labels:
                node = master[nodename]
                label = Labels[nodename]
                #
                # check if datetime is up to date
                #
                minutes_ago = now - timedelta(minutes=5)
                dt = datetime.strptime(node['datetime'], '%Y-%m-%d %H:%M:%S')
                if dt > minutes_ago:
                    temperatures[label] = node['temperature']
                    humidities[label] = node['humidity']
                else:
                    print(nodename, 'is not working since ', node['datetime'])
        print("sending...", temperatures)
        am = ambient.Ambient(TEMPERATURE_CHANNELID, TEMPERATURE_WRITEKEY)
        am.send(temperatures)
        time.sleep(5)
        print("sending...", humidities)
        am = ambient.Ambient(HUMIDITY_CHANNELID, HUMIDITY_WRITEKEY)
        am.send(humidities)

if __name__ == '__main__':
  main()
