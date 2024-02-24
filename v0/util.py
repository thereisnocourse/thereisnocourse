import time
import sys
from collections import namedtuple
from textwrap import fill
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


terminal = None


def get_terminal():
    global terminal
    if terminal is None:
        terminal = query_selector("script[terminal]").terminal
    return terminal


def clear_terminal():
    get_terminal().clear()


def pad(text, n):
    if len(text) < n:
        text += " " * (n - len(text))
    return text


def output_line(text, pause=1):
    text = fill(
        text, width=get_terminal().cols, drop_whitespace=False, replace_whitespace=False
    )
    print(text, end="", file=sys.stdout)
    sys.stdout.flush()
    time.sleep(pause)


def print_line(text, end="\n"):
    text = fill(text, width=get_terminal().cols)
    print(text, end=end, file=sys.stdout)
    sys.stdout.flush()


def output_lines(lines):
    for text, pause in lines:
        output_line(text, pause)


# ANSI colors
class ANSI:
    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    BOLD = "\u001b[1m"
    ITALICIZE = "\u001b[3m"
    UNDERLINE = "\u001b[4m"
    RESET = "\u001b[0m"


speech_pauses = {
    "para": 2,  # pause between paragraphs
    "char": 0.06,  # default pause between characters
    " ": 0.06,
    ",": 0.5,
    ";": 0.6,
    ":": 0.4,
    "—": 0.5,
    ".": 1,
    "!": 1.2,
    "?": 1.4,
    "⏸": 2,  # hidden pause
}


def speak(message):
    char_pause = speech_pauses["char"]
    para_pause = speech_pauses["para"]
    fast_forward = False
    control_symbols = {"⏵", "⏸", "⏩"}
    for line in message.split("\n"):
        for c in line:
            # Determine the length of the pause for the current character.
            pause = 0
            if c == "⏩":
                # Fast forward, suspend all pauses.
                fast_forward = True
            elif c == "⏵":
                # Back to normal play mode.
                fast_forward = False
            elif fast_forward:
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

        if not line:
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
