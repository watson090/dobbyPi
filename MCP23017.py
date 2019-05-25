#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import pigpio

REG_IODIRA = 0x00
REG_IODIRB = 0x01
REG_OLATA = 0x14
REG_OLATB = 0x15

class MCP23017(object):

    def __init__(self, bus, slave_addr):
        self._pi = pigpio.pi()
        self._bus = bus
        self._slave_addr = slave_addr

        self._state = 0x00

    def open(self):
        self._mcp23017 = self._pi.i2c_open(self._bus, self._slave_addr)

    def close(self):
        if self._pi is not None:
            self._pi.i2c_close(self._mcp23017)
            self._mcp23017 = None
    
    def output_mode(self, iodir):
        self._pi.i2c_write_device(self._mcp23017,[iodir, 0x00])

    def set_bit(self, port ,pin):
        self._state |= (1 << pin)
        self._pi.i2c_write_device(self._mcp23017, [port, self._state])        

    def reset_bit(self,port, pin):
        self._state &= ~(1 << pin)
        self._pi.i2c_write_device(self._mcp23017, [port, self._state])        
    
    def print_reg(self):
        print(bin(self._state))

if __name__ == "__main__":
    gpa1 = MCP23017(1, 0x20)
    gpb1 = MCP23017(1, 0x20)
    gpa2 = MCP23017(1, 0x21)
    gpb2 = MCP23017(1, 0x21)


    gpa1.open()
    gpb1.open()
    gpa2.open()
    gpb2.open()


    gpa1.output_mode(REG_IODIRA)
    gpb1.output_mode(REG_IODIRB)
    gpa2.output_mode(REG_IODIRA)
    gpb2.output_mode(REG_IODIRB)


    try:
        while(True):
            for i in range(8):
                gpa1.set_bit(REG_OLATA, i)
                gpb1.set_bit(REG_OLATB, i)
                gpa2.set_bit(REG_OLATA, i)
                gpb2.set_bit(REG_OLATB, i)
            time.sleep(1)
            for i in range(9):
                gpa1.reset_bit(REG_OLATA, i)
                gpb1.reset_bit(REG_OLATB, i)
                gpa2.reset_bit(REG_OLATA, i)
                gpb2.reset_bit(REG_OLATB, i)
            time.sleep(1)
    except KeyboardInterrupt:
        print("finish")
