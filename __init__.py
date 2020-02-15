"""API of common functions when writing a GUI with pygame
SEE
    https://www.pygame.org/docs/

Functions
---------
get_dev_mode() -> bool
set_dev_mode(onoff_flag=True) -> None
user_quit(event, key_pressed, key_mods) -> bool
user_opens_cmdline(key_pressed, key_mods) -> bool
user_closes_cmdline(key_pressed) -> bool
get_arg(swp) -> str
"""
from .pygameapi import *
