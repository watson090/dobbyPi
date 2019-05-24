#! /usr/bin/python
# -*- coding: utf-8 -*-

import time

import pigpio

class TackSwitch(object):
    def __init__(self, bcm_pin ,trig, func, mask_time):
        self._pi = pigpio.pi()
        self._bcm_pin = bcm_pin
        self._pi.set_mode(bcm_pin, pigpio.INPUT)
        self._pi.callback(bcm_pin, trig, self._callback_handler)

        self._mask_time = mask_time
        self._func = func

    def _callback_handler(self, gpio, level, tick):
        time.sleep(self._mask_time)
        if(self._pi.read(self._bcm_pin) == 0):
            self._func()

if __name__ == "__main__":

    def myprint():
        print("hello")

    b = TackSwitch(17, pigpio.FALLING_EDGE, myprint, 0.1)

    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
            print("Finish")
            



