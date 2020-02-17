"""--- Run unit tests from Vim: ---

VIM USAGE:
    ;ut -- run unit tests for pkgname
        - requires active buffer is test_pkgname.py
        - edit $MYVIMRC to select unittest or pytest
        - see https://docs.pytest.org/en/latest/usage.html#cmdline
"""
import pygameapi as pgui # -- module under test
# unit test framework
import unittest
import pygame
# use namedtuple to fake pygame function return values
from collections import namedtuple
# use numpy to fake pygame function return values
import numpy as np

class set_dev_mode(unittest.TestCase):
    def setUp(self):
        """Restore default state of pygameapi.
        
        Context
        -------
        pygameapi contains the line:
        DEV = False

        Intent
        ------
        Reset DEV between tests.
        DEV is global.
        Call set_dev_mode(True) changes DEV to True.
        """
        pgui.DEV=False

    def test_pgui_DOT_DEV_is_False_if_dev_UNDERSCORE_mode_is_not_called(self):
        """This test is only for generating the docstring.
        I'm not sure how to test this correctly.
        
        Issue
        -----
        Test passes even if I edit pygameapi to DEV=True.
        
        Cause
        -----
        Test setUp overrides pygameapi with pgui.DEV=False.
        """
        self.assertFalse(pgui.DEV)

    def test_pgui_DOT_DEV_is_True_if_dev_UNDERSCORE_mode_is_called_with_True(self):
        pgui.set_dev_mode(True)
        self.assertTrue(pgui.get_dev_mode())

    def test_pgui_DOT_DEV_is_True_if_dev_UNDERSCORE_mode_is_called_with_no_argument(self):
        pgui.set_dev_mode()
        self.assertTrue(pgui.get_dev_mode())

    def test_pgui_DOT_DEV_is_False_if_dev_UNDERSCORE_mode_is_called_with_False(self):
        # =====[ Setup ]=====
        pgui.set_dev_mode(True)
        # =====[ Operate ]=====
        pgui.set_dev_mode(False)
        # =====[ Test ]=====
        self.assertFalse(pgui.get_dev_mode())

class user_quit(unittest.TestCase):
    def setUp(self):
        """
        Default all tests to dev mode disabled
        --------------------------------------
        Usage:
            # Test dev mode functionality by enabling dev mode
            set_dev_mode()

        Fake syntax for a pygame 'event'
        --------------------------------
        Usage:
            event = self.Event(type=pygame.QUIT)

        Fake syntax for pygame 'boolean array of key presses'
        -----------------------------------------------------
        Usage:
            # Fake 'key_pressed==False' like this:
            # key_pressed = [T, T, T, ..., T, F]
            key_pressed = self.key_pressed != pygame.K_x
        Usage:
            # Fake 'key_pressed==True' like this:
            # key_pressed = [F, F, F, ..., F, T]
            key_pressed = self.key_pressed == pygame.K_x

        Fake modifier keys
        ------------------
        Usage:
            # Fake modifier keys held down: none
            key_mods = pygame.key.get_mods()
        Usage
            # Fake modifier keys held down: Ctrl
            pygame.key.set_mods(pygame.KMOD_CTRL)
            key_mods = pygame.key.get_mods()
        """
        # dev mode disabled
        pgui.set_dev_mode(False)

        # define event.type datatype for faking events
        self.Event = namedtuple('FakePygameEvent', ['type'])

        # define array for faking key presses by Boolean comparison
        hope_pygame_K_upper_limit = 300
        self.key_pressed = np.arange(1+hope_pygame_K_upper_limit)

        # Must init to call pygame.key.get_mods() during tests
        pygame.init()

        # no key modifiers are being held down
        pygame.key.set_mods(pygame.KMOD_NONE)

    def test_Returns_True_if_user_clicks_red_x(self):
        # =====[ Setup ]=====

        # Fake event: click red x
        event = self.Event(type=pygame.QUIT)

        # Fake key_pressed: do not press q
        key_pressed = self.key_pressed != pygame.K_q

        # Fake key_mods: none
        key_mods = pygame.key.get_mods()

        # =====[ Operate ]=====
        self.assertTrue(pgui.user_quit(event, key_pressed, key_mods))

    def test_Returns_False_if_user_presses_q_with_dev_mode_disabled(self):
        # =====[ Setup ]=====

        # Fake event: do not click red x
        event = self.Event(type=pygame.QUIT+42)

        # Fake key_pressed: press q
        key_pressed = self.key_pressed == pygame.K_q

        # Fake key_mods: none
        key_mods = pygame.key.get_mods()

        # =====[ Operate ]=====
        self.assertFalse(pgui.user_quit(event, key_pressed, key_mods))

    def test_Returns_True_if_user_presses_q_in_dev_mode(self):
        # =====[ Setup ]=====

        # Enable dev mode
        pgui.set_dev_mode()

        # Fake event: do not click red x
        event = self.Event(type=pygame.QUIT+42)

        # Fake key_pressed: press q
        key_pressed = self.key_pressed == pygame.K_q

        # Fake key_mods: none
        key_mods = pygame.key.get_mods()

        # =====[ Operate ]=====
        self.assertTrue(pgui.user_quit(event, key_pressed, key_mods))

    def test_Returns_True_if_user_presses_Ctrl_q(self):
        # Fake event: do not click red x
        event = self.Event(type=pygame.QUIT+42)
        # Fake key_pressed: press q
        key_pressed = self.key_pressed == pygame.K_q
        # Fake key_mods: hold Ctrl
        pygame.key.set_mods(pygame.KMOD_CTRL)
        key_mods = pygame.key.get_mods()
        # =====[ Operate ]=====
        self.assertTrue(pgui.user_quit(event, key_pressed, key_mods))

    def test_Returns_False_if_user_does_not_quit(self):
        # Fake event: do not click red x
        event = self.Event(type=pygame.QUIT+42)
        # Fake key_pressed: do not press q
        key_pressed = self.key_pressed != pygame.K_q
        # Fake key_mods: none
        key_mods = pygame.key.get_mods()
        # =====[ Operate ]=====
        self.assertFalse(pgui.user_quit(event, key_pressed, key_mods))

class user_opens_cmdline(unittest.TestCase):
    def setUp(self):
        # define array for faking key presses by Boolean comparison
        self.key_pressed = np.arange(1+pygame.K_SEMICOLON)

        # Must init to call pygame.key.get_mods() during tests
        pygame.init()

        # no key modifiers are being held down
        pygame.key.set_mods(pygame.KMOD_NONE)

    def test_Returns_true_if_user_presses_colon(self):
        # =====[ Setup ]=====
        # Fake user pressing colon
        # Fake by pressing SEMICOLON
        key_pressed = self.key_pressed == pygame.K_SEMICOLON
        # while holding SHIFT
        pygame.key.set_mods(pygame.KMOD_SHIFT)
        key_mods = pygame.key.get_mods()
        # =====[ Operate and Test ]=====
        self.assertTrue(pgui.user_opens_cmdline(key_pressed, key_mods))

    def test_Returns_false_if_user_does_not_press_colon(self):
        key_pressed = self.key_pressed != pygame.K_SEMICOLON
        key_mods = pygame.key.get_mods()
        self.assertFalse(pgui.user_opens_cmdline(key_pressed, key_mods))

class user_closes_cmdline(unittest.TestCase):
    def setUp(self):
        # define array for faking key presses by Boolean comparison
        self.key_pressed = np.arange(1+pygame.K_ESCAPE)

    def test_Returns_True_if_user_presses_Esc(self):
        key_pressed = self.key_pressed == pygame.K_ESCAPE
        self.assertTrue(pgui.user_closes_cmdline(key_pressed))
        
    def test_Returns_False_if_user_does_not_press_Esc(self):
        key_pressed = self.key_pressed != pygame.K_ESCAPE
        self.assertFalse(pgui.user_closes_cmdline(key_pressed))

class Window(unittest.TestCase):
    def test_Window_is_a_namedtuple_with_field_names_OPENPAREN_cols_COMMA_rows_CLOSEPAREN(self):
        self.assertEqual(pgui.Window._fields[0], 'cols')
        self.assertEqual(pgui.Window._fields[1], 'rows')

class window_size(unittest.TestCase):
    def test_Returns_tuple_width_COMMA_height(self):
        # =====[ Setup ]=====
        nc=654; nr=321
        win = pgui.Window( cols=nc, rows=nr )
        # =====[ Operate ]=====
        self.assertEqual( pgui.window_size(win), (nc,nr) )

class evaluate(unittest.TestCase):
    def test_need_to_write_some(self):
        pass
