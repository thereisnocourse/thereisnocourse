import time
import sys
from collections import namedtuple
from textwrap import TextWrapper
import js
from pyscript import document, window, when


version_info = namedtuple(
    "version_info", ("major", "minor", "micro", "releaselevel", "serial")
)
fake_version_info = version_info(0, 9, 0, "final", 0)
sys.version_info = fake_version_info
fake_version_string = "0.9.0 (Feb 20 1991)"
sys.version = fake_version_string


def debug(message):
    js.console.log(message)


def show(element, display="block"):
    element.style.display = display


def hide(element):
    element.style.display = "none"


def get_element_by_id(x):
    assert document is not None
    assert document.getElementById is not None, document
    node = document.getElementById(x)
    return node


def query_selector(selector):
    assert document is not None
    assert document.querySelector is not None, document
    result = document.querySelector(selector)
    return result


def query_selector_all(selector):
    assert document is not None
    assert document.querySelectorAll is not None, document
    result = document.querySelectorAll(selector)
    return result


def get_url_params():
    params = dict(js.URLSearchParams.new(window.location.search))
    return params


_terminal = None


def get_terminal():
    global _terminal
    if _terminal is None:
        _terminal = query_selector("script[terminal]").terminal
    return _terminal


def clear_terminal():
    get_terminal().clear()


_terminal_cols = None


def get_terminal_cols():
    global _terminal_cols
    if _terminal_cols is None:
        _terminal_cols = get_terminal().cols
    return _terminal_cols


def pad(text, n):
    if len(text) < n:
        text += " " * (n - len(text))
    return text


# ANSI colors and text formatting sequences
class ANSI:
    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    BRIGHT_BLACK = "\u001b[90m"
    BRIGHT_RED = "\u001b[91m"
    BRIGHT_GREEN = "\u001b[92m"
    BRIGHT_YELLOW = "\u001b[93m"
    BRIGHT_BLUE = "\u001b[94m"
    BRIGHT_MAGENTA = "\u001b[95m"
    BRIGHT_CYAN = "\u001b[96m"
    BRIGHT_WHITE = "\u001b[97m"
    BG_BLACK = "\u001b[40m"
    BG_RED = "\u001b[41m"
    BG_GREEN = "\u001b[42m"
    BG_YELLOW = "\u001b[43m"
    BG_BLUE = "\u001b[44m"
    BG_MAGENTA = "\u001b[45m"
    BG_CYAN = "\u001b[46m"
    BG_WHITE = "\u001b[47m"
    BG_BRIGHT_BLACK = "\u001b[100m"
    BG_BRIGHT_RED = "\u001b[101m"
    BG_BRIGHT_GREEN = "\u001b[102m"
    BG_BRIGHT_YELLOW = "\u001b[103m"
    BG_BRIGHT_BLUE = "\u001b[104m"
    BG_BRIGHT_MAGENTA = "\u001b[105m"
    BG_BRIGHT_CYAN = "\u001b[106m"
    BG_BRIGHT_WHITE = "\u001b[107m"
    BOLD = "\u001b[1m"
    ITALICIZE = "\u001b[3m"
    UNDERLINE = "\u001b[4m"
    RESET = "\u001b[0m"


# Custom coding of colors and text formatting as single unicode characters.
# This is more compact and so has less impact on wrapping of text.
class Text:
    BLACK = "\uf030"
    RED = "\uf031"
    GREEN = "\uf032"
    YELLOW = "\uf033"
    BLUE = "\uf034"
    MAGENTA = "\uf035"
    CYAN = "\uf036"
    WHITE = "\uf037"
    BRIGHT_BLACK = "\uf090"
    BRIGHT_RED = "\uf091"
    BRIGHT_GREEN = "\uf092"
    BRIGHT_YELLOW = "\uf093"
    BRIGHT_BLUE = "\uf094"
    BRIGHT_MAGENTA = "\uf095"
    BRIGHT_CYAN = "\uf096"
    BRIGHT_WHITE = "\uf097"
    BG_BLACK = "\uf040"
    BG_RED = "\uf041"
    BG_GREEN = "\uf042"
    BG_YELLOW = "\uf043"
    BG_BLUE = "\uf044"
    BG_MAGENTA = "\uf045"
    BG_CYAN = "\uf046"
    BG_WHITE = "\uf047"
    BG_BRIGHT_BLACK = "\uf100"
    BG_BRIGHT_RED = "\uf101"
    BG_BRIGHT_GREEN = "\uf102"
    BG_BRIGHT_YELLOW = "\uf103"
    BG_BRIGHT_BLUE = "\uf104"
    BG_BRIGHT_MAGENTA = "\uf105"
    BG_BRIGHT_CYAN = "\uf106"
    BG_BRIGHT_WHITE = "\uf107"
    BOLD = "\uf001"
    ITALICIZE = "\uf003"
    UNDERLINE = "\uf004"
    RESET = "\uf000"


unicode_to_ansi = str.maketrans(
    {
        Text.BLACK: ANSI.BLACK,
        Text.RED: ANSI.RED,
        Text.GREEN: ANSI.GREEN,
        Text.YELLOW: ANSI.YELLOW,
        Text.BLUE: ANSI.BLUE,
        Text.MAGENTA: ANSI.MAGENTA,
        Text.CYAN: ANSI.CYAN,
        Text.WHITE: ANSI.WHITE,
        Text.BRIGHT_BLACK: ANSI.BRIGHT_BLACK,
        Text.BRIGHT_RED: ANSI.BRIGHT_RED,
        Text.BRIGHT_GREEN: ANSI.BRIGHT_GREEN,
        Text.BRIGHT_YELLOW: ANSI.BRIGHT_YELLOW,
        Text.BRIGHT_BLUE: ANSI.BRIGHT_BLUE,
        Text.BRIGHT_MAGENTA: ANSI.BRIGHT_MAGENTA,
        Text.BRIGHT_CYAN: ANSI.BRIGHT_CYAN,
        Text.BRIGHT_WHITE: ANSI.BRIGHT_WHITE,
        Text.BG_BLACK: ANSI.BG_BLACK,
        Text.BG_RED: ANSI.BG_RED,
        Text.BG_GREEN: ANSI.BG_GREEN,
        Text.BG_YELLOW: ANSI.BG_YELLOW,
        Text.BG_BLUE: ANSI.BG_BLUE,
        Text.BG_MAGENTA: ANSI.BG_MAGENTA,
        Text.BG_CYAN: ANSI.BG_CYAN,
        Text.BG_WHITE: ANSI.BG_WHITE,
        Text.BG_BRIGHT_BLACK: ANSI.BG_BRIGHT_BLACK,
        Text.BG_BRIGHT_RED: ANSI.BG_BRIGHT_RED,
        Text.BG_BRIGHT_GREEN: ANSI.BG_BRIGHT_GREEN,
        Text.BG_BRIGHT_YELLOW: ANSI.BG_BRIGHT_YELLOW,
        Text.BG_BRIGHT_BLUE: ANSI.BG_BRIGHT_BLUE,
        Text.BG_BRIGHT_MAGENTA: ANSI.BG_BRIGHT_MAGENTA,
        Text.BG_BRIGHT_CYAN: ANSI.BG_BRIGHT_CYAN,
        Text.BG_BRIGHT_WHITE: ANSI.BG_BRIGHT_WHITE,
        Text.BOLD: ANSI.BOLD,
        Text.ITALICIZE: ANSI.ITALICIZE,
        Text.UNDERLINE: ANSI.UNDERLINE,
        Text.RESET: ANSI.RESET,
    }
)


speech_pauses = {
    "para": 2,  # pause between paragraphs
    "char": 0.06,  # default pause between characters
    " ": 0.06,
    ",": 0.5,
    ";": 0.6,
    ":": 0.7,
    "—": 0.5,
    ".": 1,
    "?": 1,
    "!": 1.2,
    "⏸": 1.6,  # hidden pause
}


def write(s, pause=0):
    """Write string `s` to stdout and flush immediately."""
    sys.stdout.write(s)
    sys.stdout.flush()
    if pause:
        time.sleep(pause)


_wrapper = None


def get_wrapper():
    global _wrapper
    if _wrapper is None:
        _wrapper = TextWrapper(
            width=min(get_terminal_cols(), 70),
            replace_whitespace=True,
            drop_whitespace=True,
        )
    return _wrapper


def fill(s):
    s = get_wrapper().fill(s)
    s = s.translate(unicode_to_ansi)
    return s


def output(s="", pause=0, end="\n"):
    s = fill(s)
    s += end
    write(s, pause=pause)


def output_help(paragraphs):
    """Standardise printing of help text."""
    output()
    for para in paragraphs:
        output(para, end="\n\n")


def speak(message):
    char_pause = speech_pauses["char"]
    para_pause = speech_pauses["para"]
    fast_forward = False
    ansi = False
    control_symbols = {"⏵", "⏸", "⏩"}
    for line in message.splitlines():
        line = fill(line)
        for c in line:
            # Determine the length of the pause for the current character.
            pause = 0
            if c == "⏩":
                # Fast forward, suspend all pauses.
                fast_forward = True
            elif c == "⏵":
                # Back to normal play mode.
                fast_forward = False
            elif c == "\u001b":
                ansi = True
            elif fast_forward or ansi:
                # Leave no pause.
                pass
            else:
                pause = speech_pauses.get(c, char_pause)

            # Print the current character.
            if c not in control_symbols:
                print(c, end="", file=sys.stdout)
                sys.stdout.flush()

            # Pause to simulate speech.
            if pause > 0:
                time.sleep(pause)

            # Terminate ANSI control sequence.
            if ansi and c == "m":
                ansi = False

        if not line and not fast_forward:
            # Empty line, interpret as gap between paragraphs.
            time.sleep(para_pause)

        # Print a line break.
        print(file=sys.stdout)
        sys.stdout.flush()


lumberjack_song = """\
I'm a lumberjack, and I'm okay
I sleep all night and I work all day
I cut down trees, I eat my lunch
I go to the lavatory
On Wednesdays I go shoppin'
And have buttered scones for tea.

I'm a lumberjack, and I'm okay
I sleep all night and I work all day
I cut down trees, I skip and jump
I like to press wild flowers
I put on women's clothing
And hang around in bars.

I'm a lumberjack, and I'm okay
I sleep all night and I work all day
I cut down trees, I wear high heels
Suspendies, and a bra
I wish I'd been a girlie
Just like my dear Papa.\
"""


function_repr_template = f"Hello, I am a function! Type {ANSI.BOLD}{{name}}(){ANSI.RESET} if you want me to do something."
