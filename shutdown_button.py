#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os, time

def shutdown(channel):
    print("shutdown button is pressed")
    os.system("sudo shutdown -h now")

def reboot(channel):
    print("reboot button is pressed")
    os.system("sudo reboot")

def main():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(4, GPIO.FALLING, callback = shutdown, bouncetime=200)
    GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(17, GPIO.FALLING, callback = reboot, bouncetime=200)

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("keyboard interrupt")
        GPIO.remove_event_detect(4)
        GPIO.remove_event_detect(17)
        GPIO.cleanup()

if __name__ == '__main__':
    main()
