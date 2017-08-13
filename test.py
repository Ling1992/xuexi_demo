# -*- coding: utf-8 -*-
import ConfigParser
import os.path
from base.config import Config
import sys



class test(object):

    def __init__(self):
        print "init"

    def __call__(self, *args, **kwargs):
        print "call;"

if __name__ == "__main__":
    aa = test()
    aa()
