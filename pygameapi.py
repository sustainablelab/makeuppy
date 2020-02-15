import pygame
from collections import namedtuple

# USEREVENTS defined by pygameapi
UI_CMD = 0

DEV = False
def get_dev_mode(): return DEV
def set_dev_mode(onoff_flag=True):
    """Enable development mode functionality.

    Behavior
    --------
    pgui.DEV is False if set_dev_mode is called with False
    pgui.DEV is False if set_dev_mode is not called
    pgui.DEV is True if set_dev_mode is called with True
    pgui.DEV is True if set_dev_mode is called with no argument

    Examples
    --------
    1. Disable dev mode
    import pygameapi as pgui
    # do nothing

    2. Enable dev mode
    import pygameapi as pgui
    pgui.set_dev_mode()         # Turn on dev mode
    # or
    pgui.set_dev_mode(True)     # Turn on dev mode

    3. Disable dev mode *after* it is enabled
    import pygameapi as pgui
    pgui.set_dev_mode(True)     # Turn on dev mode
    # ...some time later in the program...
    pgui.set_dev_mode(False)    # Turn off dev mode

    """
    global DEV
    DEV = onoff_flag

CMD = False
def get_cmd_mode(): return CMD
def set_cmd_mode(onoff_flag=True):
    global CMD
    CMD = onoff_flag

def user_quit(event, key_pressed, key_mods):
    """
    Returns True if user clicks window-close or shortcut-key quits.

    Behavior
    --------
    Returns False if user does not quit
    Returns False if user presses q with dev mode disabled
    Returns True if user clicks red x
    Returns True if user presses Ctrl q
    Returns True if user presses q in dev mode

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
    'key_mods'
        Bitmask of all modifier keys held down.
        Returned by 'pygame.key.get_mods()'.
        Use bitwise operators to test if keys are held.
        Example: key_mods & pygame.KMOD_CTRL

    Examples
    --------
    import pygameapi as pgui
    pygame.init()
    display = pygame.display.set_mode( (100,100) )
    quit = False
    while not quit:
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            quit = user_quit(event, key_pressed)
    """
    return(_user_clicked_red_x(event)
        or  (_user_held_Ctrl(key_mods)
            and _user_pressed_q(key_pressed)
            )
        or  (
            _dev( _user_pressed_q(key_pressed))
            and not _cmd()
            )
        )

def user_opens_cmdline(key_pressed, key_mods):
    """
    Behavior
    --------
    Returns false if user does not press colon
    Returns true if user presses colon
    """
    return _user_pressed_colon(key_pressed, key_mods)

def user_closes_cmdline(key_pressed):
    """
    Behavior
    --------
    Returns False if user does not press Esc
    Returns True if user presses Esc
    """
    return _user_pressed_Esc(key_pressed)

def get_arg(swp):
    """
    Return string found between '(' and ')' in input string
    'swp'.

    Returns empty string for common cases that cause Python
    built-in 'eval()' to throw an error message.

    Where possible, return a message to help the user correct
    their input expression.

    Parameters
    ----------
    'swp'
        String with parentheses
        Example: "eval('1+1')"

    Behavior
    --------
    Returns Missing ')' if input string is missing )
    Returns Missing '(' if input string is missing (
    Returns empty string if input string is ()
    Returns empty string if input string is ("")
    Returns empty string if input string is ("   ")
    Returns empty string if input string is ('')
    Returns empty string if input string is ('   ')
    Returns help message if eval expression is not a string
    Returns help message if quotes are mismatched
    Returns help message if string inside () is only one character
    Returns subset of input string that is inside parentheses

    Reference
    ---------
    https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types
    https://docs.python.org/3/library/stdtypes.html#string-methods
    """
    # Check for missing parentheses
    if swp.find('(') == -1: return ["Missing '('"]
    if swp.find(')') == -1: return ["Missing ')'"]
    # Check for mismatched parentheses
    if swp.count('(') != swp.count(')'): return [f"Missing parentheses somewhere"]
    # Get string between (), eliminate surrounding whitespace
    after_open = swp.split('(',maxsplit=1)[1]
    inside = after_open.rsplit(')',maxsplit=1)[0].strip()
    # Check for truly empty input ()
    if len(inside) == 0: return ''
    # If not empty, it must start with a quote mark
    qm = inside[0]
    # Check expression part of arg is a string
    if qm != "'" and qm != '"': return ["Expression must be a string"]
    # Check for missing closing quote
    if len(inside) == 1: return [f"Missing closing {qm}"]
    # Check for mistmatched quotes
    if inside.count(qm)%2 != 0: return [f"Missing {qm} somewhere"]
    # Check for creative ways to send empty input
    using_single_quotes = inside[0] == "'"
    using_double_quotes = inside[0] == '"'
    if using_single_quotes:
        if (
            inside.split("'")[1] == ''
            or
            inside.split("'")[1].isspace()
            ):
            return ''
    if using_double_quotes:
        if (
            inside.split('"')[1] == ''
            or
            inside.split('"')[1].isspace()
            ):
            return ''
    # Success: string inside parentheses is OK to eval... maybe...
    return inside

def evaluate(cmd):
    """
    Activate 'cmdline' with : to start a COLON command.
    Return values are displayed on the 'cmdoutput' line.

    COLON command types
    -------------------
    :eval(expression)
        Evaluate with Python builtin 'eval'
        Example:
            :eval('1+1')
            2
    """
    # COLON commands
    if cmd[0] == ':':
        # strip leading `:`
        cmd = cmd[1:]
        if cmd[0:4] == 'eval':
            # EVAL EXPRESSIONS
            empty = ''
            """
                Return an empty 'str' when:
                    The expression cannot be evaluated and there is no
                    obvious mistake to notify the user, like a missing
                    quote or parentheses.
                Examples when empty is appropriate:
                    :eval('')
                    :eval()
                    :eval("    ")
            """
            arg = get_arg(cmd)
            # arg is empty: ()
            if arg == empty: return empty
            # arg mistake is obvious
            """
                Return a 'list' when:
                    The expression cannot be evaluated and the
                    mistake is obvious.
                    List element 0 is a helpful message to display
                    in the 'cmdoutput'.
                Examples when a helpful message is appropriate:
                    :eval('print()) # user forgot "'"
                    :eval('print()' # user forgot ")"
            """
            if type(arg) == list: return arg[0]
            arg = eval(arg)
            if type(arg) == str: return eval(arg)
            # If user includes optional global dict or local dict,
            # eval(get_arg(cmd)) returns a tuple.
            if type(arg) == tuple:
                if len(arg) == 2: return eval(arg[0],arg[1])
                if len(arg) == 3: return eval(arg[0],arg[1],arg[2])
        # TODO: add more checks here for other COLON commands
        if cmd == 'start':
            # Return a user event the same as the START button press
            pass
        else: return None # unnecessary, but it makes an explicit placeholder
    # TODO: add more checks here for other types of cmdline entry
    else: return None # unnecessary, but it makes an explicit placeholder

Window = namedtuple('Window', [ 'cols', 'rows' ])

def window_size(win):
    """Return size of Window 'win' as tuple (width, height).

    Behavior
    --------
    Window is a namedtuple with field names(cols,rows)
    Returns tuple width,height

    Parameters
    ----------
    'win'
        type(win) is namedtuple 'pygameapi.Window'
        Example: win = Window( cols=1200, rows=600 )
    """
    return (win.cols, win.rows)

# Credit color scheme to Steve Losh, author of badwolf.vim
_badwolf_color_names = [
    # 'name'            (R,G,B)           ['hex', 256-color-term]
    # Normal text.
    'plain'         , # (248,246,242)   = ['f8f6f2', 15]
    # Pure and simple.
    'snow'          , # (255,255,255)   = ['ffffff', 15]
    'coal'          , # (0,0,0)         = ['000000', 16]
    # Gravel colors based on a brown from Clouds Midnight.
    'brightgravel'  , # (217,206,195)   = ['d9cec3', 252]
    'lightgravel'   , # (153,143,132)   = ['998f84', 245]
    'gravel'        , # (133,127,120)   = ['857f78', 243]
    'mediumgravel'  , # (102,100,98)    = ['666462', 241]
    'deepgravel'    , # (69,65,59)      = ['45413b', 238]
    'deepergravel'  , # (53,50,45)      = ['35322d', 236]
    'darkgravel'    , # (36,35,33)      = ['242321', 235]
    'blackgravel'   , # (28,27,26)      = ['1c1b1a', 233]
    'blackestgravel', # (20,20,19)      = ['141413', 232]
    # From highlight in photo of a glass of Dale's Pale Ale on my desk.
    'dalespale'     , # (250,222,62)    = ['fade3e', 221]
    # A beautiful tan from Tomorrow Night.
    'dirtyblonde'   , # (244,207,134)   = ['f4cf86', 222]
    # Delicious, chewy red from Made of Code for poppiest highlights.
    'taffy'         , # (255,44,75)     = ['ff2c4b', 196]
    # Another chewy accent, but use sparingly!
    'saltwatertaffy', # (140,255,186)   = ['8cffba', 121]
    # Use for things that denote 'where the user is'
    'tardis',         # (10,157,255)    = ['0a9dff', 39]
    # This one's from Mustang, not Florida!
    'orange',         # (255,167,36)    = ['ffa724', 214]
    # A limier green from Getafe.
    'lime',           # (174,238,0)     = ['aeee00', 154]
    # Rose's dress in The Idiot's Lantern.
    'dress',          # (255,158,184)   = ['ff9eb8', 211]
    # Another play on the brown from Clouds Midnight.
    'toffee',         # (184,136,83)    = ['b88853', 137]
    # Also based on that Clouds Midnight brown.
    'coffee',         # (199,145,91)    = ['c7915b', 173]
    'darkroast'       # (136,99,63)     = ['88633f', 95]
    ]
_badwolf_color_values = (
    # Normal text.
    (248,246,242),
    # Pure and simple.
    (255,255,255),
    (0,0,0),
    # Gravel colors based on a brown from Clouds Midnight.
    (217,206,195),
    (153,143,132),
    (133,127,120),
    (102,100,98),
    (69,65,59),
    (53,50,45),
    (36,35,33),
    (28,27,26),
    (20,20,19),
    # From highlight in photo of a glass of Dale's Pale Ale on my desk.
    (250,222,62),
    # A beautiful tan from Tomorrow Night.
    (244,207,134),
    # Delicious, chewy red from Made of Code for poppiest highlights.
    (255,44,75),
    # Another chewy accent, but use sparingly!
    (140,255,186),
    # Use for things that denote 'where the user is'
    (10,157,255),
    # This one's from Mustang, not Florida!
    (255,167,36),
    # A limier green from Getafe.
    (174,238,0),
    # Rose's dress in The Idiot's Lantern.
    (255,158,184),
    # Another play on the brown from Clouds Midnight.
    (184,136,83),
    # Also based on that Clouds Midnight brown.
    (199,145,91),
    (136,99,63)
    )
Color = namedtuple(
    'Color',
    _badwolf_color_names,
    defaults=_badwolf_color_values
    )

# ---Helpers---
def _dev(condition=True): return DEV and condition
def _cmd(condition=True): return CMD and condition

def _user_clicked_red_x(event): return event.type == pygame.QUIT

def _user_pressed_q(key_pressed): return key_pressed[pygame.K_q]

def _user_pressed_semicolon(key_pressed): return key_pressed[pygame.K_SEMICOLON]

def _user_pressed_Esc(key_pressed): return key_pressed[pygame.K_ESCAPE]

def _user_held_Ctrl(key_mods): return key_mods & pygame.KMOD_CTRL

def _user_held_Shift(key_mods): return key_mods & pygame.KMOD_SHIFT

def _user_pressed_colon(key_pressed, key_mods): 
    return (_user_held_Shift(key_mods)
            and _user_pressed_semicolon(key_pressed)
            )
