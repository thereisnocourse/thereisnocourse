import time
import sys
from collections import namedtuple
import js
from pyscript import document, window


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


def get_url_params():
    params = dict(js.URLSearchParams.new(window.location.search))
    return params


def output(lines):
    for text, pause in lines:
        print(text, end="", file=sys.stdout)
        sys.stdout.flush()
        time.sleep(pause)
        # time.sleep(0)


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
    for line in message.split("\n"):
        for c in line:
            if c != "⏸":
                print(c, end="", file=sys.stdout)
            sys.stdout.flush()
            pause = speech_pauses.get(c, char_pause)
            if pause > 0:
                time.sleep(pause)
        if not line:
            time.sleep(para_pause)
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