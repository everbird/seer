# -*- coding: utf-8 -*-

import sys
from os.path import dirname
SEER_PATH = dirname(dirname(__file__))
if SEER_PATH not in sys.path[0]:
    sys.path.insert(0, SEER_PATH)

from unittest2 import TestCase

from seer.helper import normallize_name

class HelperTestCase(TestCase):

    def test_normallize_name(self):
        name = '故事片:蜘蛛侠'
        result = normallize_name(name)
        self.assertEquals('蜘蛛侠', result)
