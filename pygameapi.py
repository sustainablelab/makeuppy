"""API of common functions when writing a GUI with pygame
SEE
    https://www.pygame.org/docs/
"""
import pygame

def print_is_ok():
    """Is OK."""
    print("Module import is OK.")
def user_quit(event, key_pressed):
    """Return True if user quit.
    `event`:
        list item from iterating over pygame.event.get()
    `key_pressed`:
        list returned by pygame.key.get_pressed()
        index list with constants such as pygame.K_q
