"""--- Run unit tests from Vim: ---

VIM USAGE:
    ;ut -- run unit tests for pkgname
        - requires active buffer is test_pkgname.py
"""
import pygameapi as pgui # -- module under test
# unit test framework
import unittest
import pygame
# use namedtuple to fake pygame function return values
from collections import namedtuple
# use numpy to fake pygame function return values
import numpy as np

class user_quit(unittest.TestCase):
    def setUp(self):
        # ---Fake syntax for a pygame event---
        # Usage:
        #   event = self.Event(type=pygame.QUIT)
        self.Event = namedtuple('FakePygameEvent', ['type'])
        #
        # ---Fake syntax for pygame boolean array of key presses---
        # Fake key_pressed==False as [T, T, T, ..., T, F]
        # Usage:
        #   key_pressed = self.key_pressed != pygame.K_x
        # Fake key_pressed==True  as [F, F, F, ..., F, T]
        # Usage:
        #   key_pressed = self.key_pressed == pygame.K_x
        self.key_pressed = np.arange(1+pygame.K_q)

    def test_Returns_True_if_user_clicks_red_x(self):
        # Fake event: click red x
        event = self.Event(type=pygame.QUIT)
        # Fake key_pressed: do not press q
        key_pressed = self.key_pressed != pygame.K_q
        # =====[ Operate ]=====
        self.assertTrue(pgui.user_quit(event, key_pressed))

    def test_Returns_True_if_user_presses_q(self):
        # Fake event: do not click red x
        event = self.Event(type=pygame.QUIT+42)
        # Fake key_pressed: press q
        key_pressed = self.key_pressed == pygame.K_q
        # =====[ Operate ]=====
        self.assertTrue(pgui.user_quit(event, key_pressed))

    def test_Returns_False_if_user_does_not_quit(self):
        # Fake event: do not click red x
        event = self.Event(type=pygame.QUIT+42)
        # Fake key_pressed: do not press q
        key_pressed = self.key_pressed != pygame.K_q
        # =====[ Operate ]=====
        self.assertFalse(pgui.user_quit(event, key_pressed))

