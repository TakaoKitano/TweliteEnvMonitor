#!/usr/bin/env python3
#
# readte.py: read from the TWE-Lite wireless temperature sensor and store the values
#

import serial
import re
import time
import datetime
import os
import sys
import subprocess

#
# read the value from the USB sensor device
#
def find_port():
    devicename = figure_out_device_name()
    if not devicename:
        return None

    print("reading data from ", devicename)
    port = serial.Serial(devicename, 115200)
    return port

def figure_out_device_name():
    dmesg = subprocess.check_output('dmesg').decode('utf-8')
    m = re.search(r".*FTDI USB Serial Device converter now attached to (ttyUSB\d)", dmesg)
    if m:
        devname = "/dev/" + m.group(1)
        return devname
    else:
        return None

# https://mono-wireless.com/jp/products/TWE-APPS/App_pal/parent.html
# parse raw data like this
def parse_data(raw):
    print("parse_data=", raw)
    router = raw[1:9]             
    lqi = int(raw[9:11],16)    
    sequence = int(raw[11:15],16) 
    node = raw[19:23]             
    battery = float(int(raw[39:43],16)) / float('1000')  # battery
    temperature = float(int(raw[63:67], 16)) / float('100.0')    
    humidity = float(int(raw[75:79],16)) / float('100.0')       
    return {node:{
            'datetime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sequence':sequence,
            'battery':battery,
            'temperature':temperature,
            'humidity':humidity,
            'route':{router:lqi}}}

def read_serial_port(port):
    rawdata = None
    while rawdata is None:
        try:
            rawdata = port.readline().decode("utf-8").rstrip('\n')
            # minimum check
            # first character must be ':' if rawdata is valid
            if rawdata[0] == ':':
                break
            else:
                rawdata = None
        except KeyboardInterrupt:
            print("keyboard interrupt")
            sys.exit(0)
        except:
            print("exception while reading from /dev/ttyUSB")
            time.sleep(5)
            rawdata = None
    return rawdata

def read_port(port):
    rawdata = read_serial_port(port)
    parsed = parse_data(rawdata)
    nodename = list(parsed.keys())[0]
    nodedata = parsed[nodename]
    return nodename, nodedata

if __name__ == '__main__':
    devicename = figure_out_device_name()
    if not devicename:
        print("could not detect FTDI USB Serial device")
    else:
        print(devicename)
    parsed = parse_data(':800000007B01DB8201512B02808205113008020A4111300102038F050100020A010102000219A602030004000000123093')
    nodename = list(parsed.keys())[0]
    nodedata = parsed[nodename]
    print(nodename, nodedata)
    port = find_port()
    node, data = read_port(port)
    print(node, data)
