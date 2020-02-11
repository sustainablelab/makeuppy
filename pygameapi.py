import pygame

def user_quit(event, key_pressed):
    """
    Returns True if user quit.
    User quits by clicking the red x or by keyboard shortcut.

    Parameters
    ----------
    'event'
        A message from the message list returned by
        'pygame.event.get()'.
        Quit if 'event.type' is 'pygame.QUIT'.
    'key_pressed'
        Boolean array returned by 'pygame.key.get_pressed()'.
        Use key constant values to index the array.
        Example: key_pressed[pygame.K_q]

    Examples
    --------
    quit=False
    while not quit:
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            quit = user_quit(event, key_pressed)
    """
    return(_user_clicked_red_x(event)
        or _user_pressed_q(key_pressed)
        )

def _user_clicked_red_x(event): return event.type == pygame.QUIT

# TODO: set package attribute to turn this 'dev' shortcut off.
def _user_pressed_q(key_pressed): return key_pressed[pygame.K_q]
