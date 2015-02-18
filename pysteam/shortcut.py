#!/usr/bin/env python
# encoding: utf-8
"""
shortcut.py

Created by Scott on 2013-12-28.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

from pysteam import game
from pysteam._crc_algorithms import Crc

class Shortcut(game.Game):

    def __init__(self, name, exe, startdir, icon="", tags=None):
        if tags is None:
          tags = []
        self.name = name
        self.exe = exe
        self.startdir = startdir
        self.icon = icon
        self.tags = tags

    def __eq__(self, other):
        return (self.name == other.name and
                self.exe == other.exe and
                self.startdir == other.startdir and
                self.icon == other.icon and
                self.tags == other.tags)

    def appid(self):
        algorithm = Crc(width = 32, poly = 0x04C11DB7, reflect_in = True, xor_in = 0xffffffff, reflect_out = True, xor_out = 0xffffffff)
        crc_input = ''.join([self.exe,self.name])
        top_32 = algorithm.bit_by_bit(crc_input) | 0x80000000
        full_64 = (top_32 << 32) | 0x02000000
        return str(full_64)