#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import signal
import datetime

import pigpio

import TactSwitch

table = [7, 6, 5, 4, 3, 2, 1, 0, 8, 9, 10, 11, 12, 13, 14, 15]

def set_lift_callback():
    print("set lift state")

def reset_lift_callback():
    global wif_file
    global log
    global current_line_number
    outputLifts = [0] * 32
    
    data = wif_file.readline()
    data_str = re.split(r"[=,\n]", data)
    lifts = map(int,data_str[1:-1])
    current_line_number += 1

    log.write(str(current_line_number) + '\n')
    print(current_line_number, lifts)
    for lift in lifts:
        outputLifts[lift-1] = 1
    print(outputLifts)
    print('\n')
    

if __name__ == "__main__":
    args = sys.argv
    if(len(args) < 2):
        print("ERROR: missing argumenrs")

    wif_file_name = args[1]
    current_line_number = int(args[2])

    wif_file = open("./resource/" + wif_file_name)
    log = open("log.txt", 'w')
    log.write(str(datetime.datetime.today()) + '\n')

    for i in range(current_line_number):
        print(i + 1, wif_file.readline())
    
    yellow_sw = TactSwitch.TactSwitch(17, pigpio.FALLING_EDGE, reset_lift_callback, 0.1)

    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        wif_file.close()
        log.close()
        print("finish")

    
