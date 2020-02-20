import pygame
import pygame_gui
from collections import namedtuple
import sys # catch and return eval errors as string instead of halting
import os # get path to this package

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

def get_fullscreen_Window(): # -> makeuppy.Window
    """
    Return the fullscreen window size as a makeuppy.Window.
    Call this once at the beginning of the program and save this
    size in a global `Window`.
    Return to fullscreen using this global.

    Context
    -------
    Call this at the beginning of the application. This is the
    only time that 'pygame.display.Info()' returns the correct
    screen size.

    Use this window size later when switching to fullscreen.
    Example:
    """
    gui_display = pygame.display.set_mode( # -> Surface
        flags=(pygame.FULLSCREEN) # can't tell a difference setting additional flags
        )
    video_info = pygame.display.Info()
    fullscreen_window = Window(cols=video_info.current_w, rows=video_info.current_h)
    # print(f"video_info.current_w -> {video_info.current_w}")
    # print(f"video_info.current_h -> {video_info.current_h}")
    return fullscreen_window

def make_screensize(size=(640, 480), is_fullscreen=False): # -> Surface
    """Change GUI window to 'size' and control if 'fullscreen' is on/off.

    For windowed (not fullscreen), application should:
    - control window size using os.environ to set SDL environment variable
    - set a caption for the window

    Returns new 'Surface' created by 'pygame.display.set_mode()'

    With no arguments, make_screensize() defaults to a 640x480 window.

    Parameters
    ----------
    size:
        tuple (cols, rows)
        Instead of remembering if columns are width or height, use Window:
        - make namedtuple: mywindow = makeuppy.Window
        - pass the window size with makeuppy.window_size(mywindow)
    is_fullsize:
        bool
        if True:
            sets flag pygame.FULLSCREEN in call to pygame.display.set_mode()
        if False:
            puts icon in window

    Example for windowed view
    -------------------------
    # Early in the program, set a window size to use when not fullscreen
    # for passing later when creating UI elements
    windowed = makeuppy.Window(cols=640, rows=480)
    #...
    # Later when switching window size:
    make_screensize(makeuppy.window_size(windowed), is_fullscreen=False)

    Example for fullscreen
    ----------------------
    # At start of program, get window size for fullscreen.
    # This MUST go in a variable:
    # The function returns wrong value after window is not fullscreen!
    fullscreen = makeuppy.get_fullscreen_Window()
    #...
    # Later when switching window to fullscreen
    make_screensize(makeuppy.window_size(fullscreen), is_fullscreen=True)
    """
    if is_fullscreen:
        gui_display = pygame.display.set_mode( # -> Surface
            size, # -> (width, height)
            flags=(pygame.FULLSCREEN)
            )
    else:
        gui_display = pygame.display.set_mode( # -> Surface
            size # -> (width, height)
            )
        set_icon() # not visible if fullscreen
    return gui_display

_pygameapi_path = os.path.dirname(__file__)
_costume_path = os.path.join(_pygameapi_path, 'costume')
# ROOT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# THEME_PATH = os.path.normpath(os.path.join(ROOT_PATH, 'data/default_theme.json'))
def set_icon(icon=f'{_costume_path}/mike-icon.jpg'):
    """Use this icon in upper left of window.

    Icon is not visible in fullscreen mode.
    """
    pygame.display.set_icon(pygame.image.load(icon))

def new_ui_manager(gui_win, theme=f'{_costume_path}/theme.json'):
    """Return a new instance of the pygame_gui UIManager.

    I made this wrapper to set my default theme.json.
    """
    return pygame_gui.UIManager(window_size(gui_win), theme)

def get_rect_height_for_gapless_cmdline(manager): # -> Int
    """ Return rect height value in pixels so UITextEntryLine instances stack
    vertically without gaps.

    Use returned height value to eliminate gaps between vertically stacked
    instances of UITextEntryLine. This makes the command line look like a single
    entity.
    
    Context
    -------
    Application command line is made of two UITextEntryLine instances:
        - cmdline respsone prints on bottom line
        - user cmdline input is on top line
    The two UITextEntryLine instances sit at the bottom of the window.

    The font and font size are set in the theme.json file.
    
    Algorithm
    ---------
    Rectangle height for gapless stacking is found by adding 4 to the height of
    any invisible character: \s, \t, \n

    Parameters
    ----------
    manager:
        Instance of pygame_gui.UIManager that controls the command line UI
        elements.

    Example
    -------
    # Earlier setup for sizing application window
    # -------------------------------------------
    # Find out the size for fullscreen
    fullscreen = makeuppy.get_fullscreen_Window()
    # When not fullscreen, use 640x480
    windowed = makeuppy.Window(cols=640, rows=480)
    # Decide if application starts in fullscreen
    is_fullscreen = False
    #
    # ...
    #
    # Setting up GUI elements
    # -----------------------
    # Make a GUI manager
    manager = makeuppy.new_ui_manager(fullscreen if is_fullscreen else windowed)
    cmdline_height = makeuppy.get_rect_height_for_gapless_cmdline(manager)
    """
    dummy = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect(
            (0,0), # rect left,top
            (50,0), # rect width,height (height set by font-size)
            ),
        manager=manager
        )
    # Find out the tallest character:
    height = dummy.font.size('\n')[1] + 4
    '''
    Example heights
    ---------------
    Consolas 14 pt: 19 pixels tall
    Consolas 18 pt: 23 pixels tall
    '''
    dummy.kill()
    return height

def make_cmdline(manager, current_Window, stack_level): # -> UITextEntryLine
    """Return UI element for a part of the command line.

    Parameters
    ----------
    manager:
        ui_manager that controls this UI element

    current_Window:
        type: namedtuple makeuppy.Window
        UI element width is sized to fill the width of this
        Window.
        Use the current window setting (either fullscreen or a
        640x480 window) so that the element fills the current
        window.

    stack_level:
        type: int
        stack_level=1: bottom line, e.g., the command output
        stack_level=2: next line up, e.g., the command input

    Returns an instance of UITextEntryLine.

    Appearance
    ----------
    'ui_text_entry_line.py' see '# colours from theme'
    Color (Colour):
        Normal text:
        text_colour: normal_text, use 'lightgravel'
        background_colour: dark_bg, use 'blackgravel'
        Selected text: (inverse of normal text)
        selected_text_colour: selected_text, use 'blackgravel'
        selected_bg_colour: selected_bg, use 'lightgravel'

    Font
        Not sure how to select when to use regular/bold/italic,
        etc. Just picking ones I like and using them as the
        "regular_path" in theme.json.

        "size": "18",
        "regular_path": "font/Consolas-Font/CONSOLAB.TTF"
        B is for bold.

        Font file must be placed in this path relative to the
        application:
            font/
        And application must be run with pwd set to its folder
        for this relative path to work.

        Get fonts without licensing issues
        ----------------------------------
        Download free fonts from these two sites. Check license
        before downloading.

        https://freefontsfamily.com/
        https://www.1001freefonts.com/

        Do not use built-in Windows fonts because you are not
        allowed to distribute the built-in Windows fonts with
        software, and I'm not sure how to set the font without
        putting a copy of it in with this application.
    """
    cmdline = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        relative_rect=pygame.Rect(
            (0,current_Window.rows-stack_level*get_rect_height_for_gapless_cmdline(manager)), # left,top is at bottom-left corner of window
            (current_Window.cols,0), # width, height is at full-width, height set by font-size (input ignored)
            ),
        manager=manager
        )
    return cmdline

def resize_cmdline(cmdline_ui_element, current_Window, stack_level, manager):
    """Resize by kill and make again. Preserve text and color.

    TODO
    ----
    Make cmdline into an obejct so the trailing parameters are
    all know from the object itself:
    - current_Window
    - stack_level
    - manager that owns this ui element
    """
    save_text = cmdline_ui_element.get_text()
    save_textcolour = cmdline_ui_element.text_colour
    cmdline_ui_element.kill()
    cmdline = make_cmdline(manager, current_Window, stack_level)
    cmdline.set_text(save_text)
    cmdline.text_colour = save_textcolour
    return cmdline

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

def evaluate(cmd):
    """
    Activate 'cmdline' with : to start a COLON command.
    Return values are displayed on the 'cmdoutput' line.

    'evaluate(cmd)' returns a string (at best).
    It is up to the application to make the commands do something
    useful.

    Some commands do not even return a string.

    COLON command types
    -------------------
    :eval(expression)
        Evaluate with Python builtin 'eval'.
        Response to eval is an empty string to let the
        application perform the eval:

        Application Snippet
        -------------------
        if event.text.startswith(':'): cmdtext = event.text[1:]
            if cmdtext[0:4] == 'eval':
                try: cmdoutput.set_text(str(eval(cmdtext)))
                except:
                    cmdoutput.text_colour = pygame.Color(color_hex.tardis)
                    cmdoutput.set_text(str(sys.exc_info()[1]))

        The benefit of 'eval' is to call application functions.
        The idea is to make the GUI like a REPL with all the
        application globals imported.

        To make the application functions visible to 'eval', it
        must be called in the application, i.e., 'eval' is useful
        when eval('__name__') returns __main__. 'eval' is not
        useful when eval('__name__') returns pygameapi.pygameapi

        Example: (command line responses)
            :eval('1+1')
            2

            :eval('1+x',{'x':3})
            4

            :eval('1+x+a_local',{'x':5},{'a_local':2})
            8

            :eval('__name__')
            __main__

            :eval(__name__)
            name '__main__' is not defined

    :echo(expression)
        Calls 'eval' on 'expression'.

        Unlike ':eval', ':echo' calls 'eval' inside pygameapi.
        The application does not require any additional code to
        make ':echo' work. Simply output the response from calling
        evaluate(cmd).

        Since the 'eval' is done inside pygameapi, 'echo' is only
        useful for toy examples. But the command line gets a more
        flexible than with 'eval'. It is useful for doing quick
        math at the command line.

        Example: (command line responses)
            :echo '1+1'
            '1+1'

            :echo (1+1)
            2

            :echo 1+1
            2

            :echo __name__
            pygameapi.pygameapi

    :start
        Command to start the monochromator sweep.
        Return an 'OK' message.
    
        Application Snippet -- Producer
        -------------------
        # Generate event, like clicking a START button
        if cmd == 'start': # press button
            start_sweep = pygame.event.Event(
                pygame.USEREVENT,
                    {'user_type': pgui.UI_CMD,
                     'ui_cmd': cmd
                    })
                    pygame.event.post(start_sweep)

        Application Snippet -- Consumer
        -------------------
        # Consume event
        if event.type == pygame.USEREVENT:
            if event.user_type == pgui.UI_CMD and event.ui_cmd == 'start':
                pass # put code here to start collecting data

        Application Snippet -- View
        -------------------
        # Format response to ':start' returned by evaluate(cmd)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:

                # Stop blinking the cursor on the command line
                if cmdline.selected: manager.unselect_focus_element()

                # Default color for responses
                cmdoutput.text_colour = save_color

                # Get response by calling 'evaluate()'
                response = str(pgui.evaluate(event.text))

                # Format the response
                if response.startswith('ERROR'):
                    # Color ERROR responses red
                    cmdoutput.text_colour = pygame.Color(color_hex.taffy)
                elif response.startswith('OK'):
                    # Color OK responses green
                    cmdoutput.text_colour = pygame.Color(color_hex.saltwatertaffy)
                    # Strip the "OK: " from the response message
                    response = response.lstrip('OK: ')
    """
    # Catch 0-length commands (happens if user erases ':' and hits ENTER)
    empty = ''
    if len(cmd) == 0: return empty
    # COLON commands
    if cmd.startswith(':'):
        # strip leading `:`
        cmd = cmd[1:]
        if cmd[0:4] == 'eval': return empty
        # TODO: add more checks here for other COLON commands
        if cmd == 'q':
            # Return a user event same as quitting
            return empty
        if cmd.startswith('echo'):
            args = cmd.lstrip('echo').strip()
            try: return eval(args)
            except: return "ERROR: " + str(sys.exc_info()[1])
        if cmd == 'start':
            # Application returns a user event the same as the
            # START button press.
            # This package just returns a message.
            return 'OK: Starting monochromator sweep...'
        # else: return None # unnecessary, but it makes an explicit placeholder
        else: return 'ERROR: Command not recognized'
    # TODO: add more checks here for other types of cmdline entry
    # else: return None # unnecessary, but it makes an explicit placeholder
    else: return 'ERROR: Start commands with colon (:)'

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
_badwolf_color_HEX_values = (
    # Normal text.
    '#f8f6f2',
    # Pure and simple.
    '#ffffff',
    '#000000',
    # Gravel colors based on a brown from Clouds Midnight.
    '#d9cec3',
    '#998f84',
    '#857f78',
    '#666462',
    '#45413b',
    '#35322d',
    '#242321',
    '#1c1b1a',
    '#141413',
    # From highlight in photo of a glass of Dale's Pale Ale on my desk.
    '#fade3e',
    # A beautiful tan from Tomorrow Night.
    '#f4cf86',
    # Delicious, chewy red from Made of Code for poppiest highlights.
    '#ff2c4b',
    # Another chewy accent, but use sparingly!
    '#8cffba',
    # Use for things that denote 'where the user is'
    '#0a9dff',
    # This one's from Mustang, not Florida!
    '#ffa724',
    # A limier green from Getafe.
    '#aeee00',
    # Rose's dress in The Idiot's Lantern.
    '#ff9eb8',
    # Another play on the brown from Clouds Midnight.
    '#b88853',
    # Also based on that Clouds Midnight brown.
    '#c7915b',
    '#88633f',
    )
_badwolf_color_RGB_values = (
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
ColorRGB = namedtuple(
    'ColorRGB',
    _badwolf_color_names,
    defaults=_badwolf_color_RGB_values
    )
ColorHEX = namedtuple(
    'ColorHEX',
    _badwolf_color_names,
    defaults=_badwolf_color_HEX_values
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
