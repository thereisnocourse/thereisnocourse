from enum import Enum
from util import (
    when,
    get_element_by_id,
    show,
    hide,
    write,
    output,
    get_terminal,
    speak,
    function_repr_template,
    ANSI,
)
import code


class InteractionComplete(SystemExit):
    pass


loading_node = get_element_by_id("loading")
play_button_node = get_element_by_id("play_button")
prologue_node = get_element_by_id("prologue")
screen_node = get_element_by_id("screen")
terminal = get_terminal()


Location = Enum("Location", ["OUTSIDE", "HALL", "DUNGEON", "BEDROOM", "BATTLEMENTS"])


def play():
    hide(prologue_node)
    screen_node.style.visibility = "visible"

    write(f"\n{ANSI.BOLD}")
    speak("   || The Scottish Play")
    speak(f"===||========={ANSI.BG_RED}=======>>{ANSI.RESET}")
    speak(f"{ANSI.BOLD}   ||")
    write(f"{ANSI.RESET}\n")
    speak(
        f"""\
Type {ANSI.BOLD}help(){ANSI.RESET} for the game tutorial.
---"""
    )

    while not game_state["game_over"]:
        location = game_state["location"]
        if location == Location.OUTSIDE:
            play_outside()
        elif location == Location.HALL:
            play_hall()
        elif location == Location.DUNGEON:
            play_dungeon()
        elif location == Location.BEDROOM:
            play_bedroom()
        elif location == Location.BATTLEMENTS:
            play_battlements()
        else:
            raise RuntimeError("unexpected location")

    game_completed()


class Newspaper:
    """Newspapers are good for reading."""

    def __repr__(self):
        return "It's today's newspaper.\n"

    def __str__(self):
        return "newspaper"

    def use(self):
        # There are no preconditions, the newspaper can be used at
        # any time in the game.
        output()
        speak(
            f"""\
14 August 1040

{ANSI.BOLD}MACDONWALD DEFEATED{ANSI.RESET}

Dunguido Macrossum, King of Scotland, has defeated the rebel Macdonwald of the Western Isles and his ally Sweno, King of Norway.

Led by his captains Macbeth and Banquo, King Dunguido's army dealt a decisive blow and ended the revolt.

A sergeant in the King's army said:

{ANSI.ITALICIZE}For brave Macbeth (well he deserves that name),
Disdaining Fortune, with his brandished steel,
Which smoked with bloody execution,
Like Valor's minion, carved out his passage
Till he faced the slave;
Which ne'er shook hands, nor bade farewell to him,
Till he unseamed him from the nave to th' chops,
And fixed his head upon our battlements.{ANSI.RESET}

Macbeth will now travel to the King's castle to celebrate the victory.
"""
        )


class Torch:
    """Torches help to shed light in the darkness."""

    def __repr__(self):
        return "It's a flaming torch.\n"

    def __str__(self):
        return "torch"


class FrontDoor:
    """You could use the front door to enter the castle."""

    def __repr__(self):
        return "The front door of the castle.\n"

    def __str__(self):
        return "door"

    def use(self):
        location = game_state["location"]
        if location == Location.OUTSIDE:
            game_state["location"] = Location.HALL
        elif location == Location.HALL:
            game_state["location"] = Location.OUTSIDE
        raise InteractionComplete


class HelpFunction:
    """Type help() for the in-game tutorial. Type help(X) to get a hint about how to use object X. But then you already knew that :)"""

    def __repr__(self):
        return function_repr_template.format(name="help") + "\n"

    def __call__(self, *args):
        if len(args) == 0:
            self._tutorial()
        elif len(args) == 1:
            arg = args[0]
            output(arg.__doc__)
            output()

    def _tutorial(self):
        output()
        speak(
            f"""\
In each location you will find some objects. These objects can be used to help you on your quest for power and glory.

To look at an object, type the name of the object and press return. For example, to look at the {ANSI.BOLD}newspaper{ANSI.RESET}:⏩
              
>>> ⏵⏸newspaper
              
To get help on how to use an object, type {ANSI.BOLD}help(X){ANSI.RESET} where {ANSI.BOLD}X{ANSI.RESET} is the name of an object. For example:⏩
              
>>> ⏵⏸help(newspaper)

To use an object, type {ANSI.BOLD}use(X){ANSI.RESET} where {ANSI.BOLD}X{ANSI.RESET} is the name of an object. For example:⏩
              
>>> ⏵⏸use(newspaper)

To take an object and carry it with you to the next location, type {ANSI.BOLD}take(X){ANSI.RESET} where {ANSI.BOLD}X{ANSI.RESET} is the name of an object. For example:⏩

>>> ⏵⏸take(newspaper)
              
At any point in the game you can {ANSI.BOLD}sing(){ANSI.RESET} if you feel like it.

{ANSI.ITALICIZE}But screw your courage to the sticking place
And we'll not fail!{ANSI.RESET}
""",
        )


class TakeFunction:
    """Type take(X) to pick up object X and carry it with you to the next location."""

    def __repr__(self):
        return function_repr_template.format(name="take") + "\n"

    def __call__(self, *args):
        if len(args) == 0:
            output("Did you mean to take something?")
            output()
        for o in args:
            self._take(o)

    def _take(self, o):
        location = game_state["location"]
        available = game_state[location]
        holding = game_state["holding"]

        if o in holding:
            output(f"You are alreading holding the {o}.")
        elif o not in available:
            output(f"The {o} is not available.")
        elif o in fixed:
            output(f"The {o} cannot be taken.")
        else:
            available.remove(o)
            holding.add(o)
            output(f"You have taken the {o}.", 1)
            output()
            status()
        output()


class UseFunction:
    """Type use(X) to try and use object X."""

    def __repr__(self):
        return function_repr_template.format(name="use") + "\n"

    def __call__(self, *args):
        if len(args) == 0:
            output("Did you mean to use something?")
            output()
        for o in args:
            if hasattr(o, "use"):
                o.use()
            else:
                output(f"Object {o} cannot be used.")


class SingFunction:
    """Type sing() if you feel like singing!"""

    def __repr__(self):
        return function_repr_template.format(name="sing") + "\n"

    def __call__(self, *args):
        pass


newspaper = Newspaper()
torch = Torch()
front_door = FrontDoor()
help = HelpFunction()
take = TakeFunction()
use = UseFunction()
sing = SingFunction()


# Initial game state.
game_state = {
    "location": Location.OUTSIDE,
    Location.OUTSIDE: {newspaper, torch, front_door},
    Location.HALL: {front_door},
    "holding": set(),
    "hall_lit": False,
    "prophecy_heard": False,
    "computer_destroyed": False,
    "forest_defeated": False,
    "game_over": False,
}


# These objects cannot be taken.
fixed = {front_door}


def status():
    location = game_state["location"]
    available = game_state[location]
    holding = game_state["holding"]
    available_str = ", ".join([str(o) for o in available])
    holding_str = ", ".join([str(o) for o in holding])
    output(f"Objects available: [{ANSI.BOLD}{available_str}{ANSI.RESET}]", 1)
    output(f"Objects held: [{ANSI.BOLD}{holding_str}{ANSI.RESET}]", 1)

    namespace = dict()
    for o in available:
        namespace[str(o)] = o
    for o in holding:
        namespace[str(o)] = o
    namespace["help"] = help
    namespace["take"] = take
    namespace["use"] = use
    namespace["sing"] = sing
    return namespace


def play_outside():
    output()
    output("You are standing outside a castle.", 1)
    output()
    namespace = status()
    output()

    try:
        code.interact(local=namespace, banner="")
    except InteractionComplete:
        pass


def play_hall():
    output()
    output("You are in the main hall.", 1)
    output()
    namespace = status()
    output()

    try:
        code.interact(local=namespace, banner="")
    except InteractionComplete:
        pass


def play_dungeon():
    pass


def play_bedroom():
    pass


def play_battlements():
    pass


def game_completed():
    pass


@when("click", "#play_button")
def play_button_on_click(event):
    play()


if __name__ == "__main__":
    hide(loading_node)
    show(play_button_node)
    play()
