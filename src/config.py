#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser

cfgfile = "../config.cfg"

parser = ConfigParser.SafeConfigParser()
parser.read(cfgfile)


def write():
    with open(cfgfile, 'wb') as write_file:
        parser.write(write_file)
