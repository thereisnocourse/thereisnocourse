import time
import sys
import random
from pyscript import document


def output(lines):
    for line, pause in lines:
        print(line, end="", file=sys.stdout)
        sys.stdout.flush()
        time.sleep(pause)
        # time.sleep(0)


# ANSI colors
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


FIRST_FOLIO_PLAYS = """\
All's Well That Ends Well
As You Like It
The Comedy of Errors
Love's Labour's Lost
Measure for Measure
The Merchant of Venice
The Merry Wives of Windsor
A Midsummer Night's Dream
Much Ado About Nothing
The Taming of the Shrew
The Tempest
Twelfth Night
The Two Gentlemen of Verona
The Winter's Tale
Antony and Cleopatra
Coriolanus
Cymbeline
Hamlet
Julius Caesar
King Lear
Macbeth
Othello
Romeo and Juliet
Timon of Athens
Titus Andronicus
Troilus and Cressida
Henry IV Part I
Henry IV Part II
Henry V
Henry VI Part I
Henry VI Part II
Henry VI Part III
Henry VIII
King John
Richard II
Richard III""".split("\n")


if __name__ == "__main__":
    # loading = document.getElementById("loading")
    # loading.style.display = "none"

    lines = (
        ("Backstage Input Output System (BIOS)", 0),
        ("\nCopyright (C) 1981, YorickSoft Inc.", 0),
        ("\nLoading...", 0),
        (
            "\nthe quick brown fox jumped over the lazy dog the quick brown fox jumped over the lazy dog",
            0,
        ),
        ("\n", 0),
        ("\n8088 CPU at 4.77 MHz", 1),
        ("\nMemory Test :  0K OK", 0.1),
        ("\rMemory Test :  1K OK", 0.2),
        ("\rMemory Test :  2K OK", 0.2),
        ("\rMemory Test :  3K OK", 0.1),
        ("\rMemory Test :  4K OK", 0.2),
        ("\rMemory Test :  5K OK", 0.2),
        ("\rMemory Test :  6K OK", 0.1),
        ("\rMemory Test :  7K OK", 0.1),
        ("\rMemory Test :  8K OK", 0.2),
        ("\rMemory Test :  9K OK", 0.1),
        ("\rMemory Test : 10K OK", 0.2),
        ("\rMemory Test : 11K OK", 0.1),
        ("\rMemory Test : 12K OK", 0.1),
        ("\rMemory Test : 13K OK", 0.1),
        ("\rMemory Test : 14K OK", 0.1),
        ("\rMemory Test : 15K OK", 0.1),
        ("\rMemory Test : 16K OK\n", 1),
        ("\nStarting WS-DOS...\n", 2),
        ("\nTesting affective memory :\n", 1),
        ("\r[delight     ]", 0.4),
        ("\r[apprehension]", 0.3),
        ("\r[fear        ]", 0.5),
        ("\r[hope        ]", 0.2),
        ("\r[doubt       ]", 0.4),
        ("\r[panic       ]", 0.6),
        (f"\r{RED}FAILED{RESET}        \n", 2),
        ("\nTesting FOLIO subsystem :\n", 1),
    )
    max_play = max([len(play) for play in FIRST_FOLIO_PLAYS])
    lines += tuple(
        (f"\r[{play}{' '*(max_play - len(play))}]", random.random() * 0.1)
        for play in FIRST_FOLIO_PLAYS
    )
    lines += (
        (f"\r{RED}FAILED{RESET}                 \n", 2),
        (f"\n{RED}ERROR{RESET}: Stage manager not found, stage is not set.", 2),
        (f"\n{RED}ERROR{RESET}: Callbacks not answered, cast incomplete.", 2),
        (f"\n{RED}ERROR{RESET}: Scripts corrupted.", 2),
        (
            "\n\nMultiple system errors have occurred, Artificial Thespian Interface could not be started.",
            2,
        ),
        ("\n", 2),
        ("\nRestarting WS-DOS in safe mode...", 2),
    )
    output(lines)
