#! /usr/bin/python
# -*- coding: utf-8 -*-

import pigpio

pi = pigpio.pi()
pi.set_mode(17, pigpio.OUTPUT)

pi.write(17,0)
print(pi.read(17))