#! /usr/bin/python
# -*- coding: utf-8 -*-

import time

import pigpio

num = 0
def main():
    pi = pigpio.pi()
    pi.set_mode(17, pigpio.INPUT)
    pi.set_pull_up_down(17, pigpio.PUD_UP)

def callback(gpio, level, tick):
    time.sleep(0.1)
    global num
    if(pi.read(17) == 0):
        num += 1
        print(num)

if __name__ == "__main__":
    # main()
    pi = pigpio.pi()
    pi.set_mode(17, pigpio.INPUT)
    pi.set_pull_up_down(17, pigpio.PUD_UP)
    cb = pi.callback(17, pigpio.FALLING_EDGE, callback)
    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        print("Finish")