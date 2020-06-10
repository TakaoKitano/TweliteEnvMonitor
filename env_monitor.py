#!/usr/bin/env python3
#
# env_monitor.py: read from the TWE-Lite wireless temperature sensor and store the values
#
import time
import datetime
import os
import sys
import json
import shutil
from device_utils import find_port
from device_utils import read_port

import appenv

def main():
    port = find_port()
    if not port:
        print("no FTDI USB serial device found")
        time.sleep(5)	
        sys.exit()

    master = {}
    while True:
        #
        # update master
        #
        nodename, nodedata = read_port(port)
        print(nodename, ':', nodedata)
        if nodename in master:
            #
            # if we already have a same sequence data, 
            # merge route data
            #
            node = master[nodename]
            if node['sequence'] == nodedata['sequence']:
                nodedata['route'].update(node['route'])
        master[nodename] = nodedata
 
        #
        # update master file
        # As master.json could be accessed by other process, 
        # we need an atomic file update
        # 
        tmpfile = appenv.FILENAME_MASTER + ".tmp"
        with open(tmpfile, "w") as f:
            json.dump(master, f, indent=4)
        shutil.move(tmpfile, appenv.FILENAME_MASTER)

if __name__ == '__main__':
    main()
