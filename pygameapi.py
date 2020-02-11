import pygame

def print_is_ok():
    """Is OK."""
    print("Module import is OK.")
def user_quit(event, key_pressed):
    """Return True if user quit.
    event:
        - a message from the message list
          returned by pygame.event.get()
    key_pressed:
        - array of booleans returned by pygame.key.get_pressed()
        - use key constant values to index the array
          example: key_pressed[pygame.K_q]
    USAGE:
        quit=False
        while not quit:
            for event in pygame.event.get():
                key_pressed = pygame.key.get_pressed()
                quit = user_quit(event, key_pressed)
    """
