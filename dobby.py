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
import MCP23017

# table = [7, 6, 5, 4, 3, 2, 1, 0, 8, 9, 10, 11, 12, 13, 14, 15]
tablea = [7, 6, 5, 4, 3, 2, 1, 0]
tableb = [0, 1, 2, 3, 4, 5, 6, 7]
gpa1 = MCP23017.MCP23017(1, 0x20)
gpb1 = MCP23017.MCP23017(1, 0x20)
gpa2 = MCP23017.MCP23017(1, 0x21)
gpb2 = MCP23017.MCP23017(1, 0x21)

def init_mcp23017():
    gpa1.open()
    gpb1.open()
    gpa2.open()
    gpb2.open()

    gpa1.output_mode(MCP23017.REG_IODIRA)
    gpb1.output_mode(MCP23017.REG_IODIRB)
    gpa2.output_mode(MCP23017.REG_IODIRA)
    gpb2.output_mode(MCP23017.REG_IODIRB)


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

    for i in range(8):
        if outputLifts[i]:
            gpa1.set_bit(MCP23017.REG_OLATA, tablea[i])
        else:
            gpa1.reset_bit(MCP23017.REG_OLATA, tablea[i])
    for i in range(8,16):
        if outputLifts[i]:
            gpb1.set_bit(MCP23017.REG_OLATB, tableb[i-8])
        else:
            gpb1.reset_bit(MCP23017.REG_OLATB, tableb[i-8])
    for i in range(16,24):
        if outputLifts[i]:
            gpa2.set_bit(MCP23017.REG_OLATA, tablea[i-16]) 
        else: 
            gpa2.reset_bit(MCP23017.REG_OLATA, tablea[i-16])
    for i in range(24,32):
        if outputLifts[i]:
            gpb2.set_bit(MCP23017.REG_OLATB, tableb[i-24]) 
        else: 
            gpb2.reset_bit(MCP23017.REG_OLATB, tableb[i-24])


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

    init_mcp23017()

    for i in range(current_line_number):
        print(i + 1, wif_file.readline())
    
    yellow_sw = TactSwitch.TactSwitch(17, pigpio.FALLING_EDGE, reset_lift_callback, 0.1)

    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        wif_file.close()
        log.close()
        gpa1.close()
        gpb1.close()
        gpa2.close()
        gpb2.close()


        print("finish")

    
