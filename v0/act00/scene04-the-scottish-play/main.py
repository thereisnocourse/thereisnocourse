from util import (
    when,
    get_element_by_id,
    show,
    hide,
    write,
    output,
    output_help,
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


def play():
    hide(prologue_node)
    screen_node.style.visibility = "visible"

    #     write(f"\n{ANSI.BOLD}")
    #     speak("   || The Scottish Play")
    #     speak(f"===||========={ANSI.BG_RED}=======>>{ANSI.RESET}")
    #     speak(f"{ANSI.BOLD}   ||")
    #     write(f"{ANSI.RESET}\n")
    #     speak(
    #         f"""\
    # Type {ANSI.BOLD}help(){ANSI.RESET} for the game tutorial.
    # ---"""
    #     )

    while not game_state["game_over"]:
        location = game_state["location"]
        if location == "outside":
            play_outside()
        elif location == "hall":
            play_hall()
        elif location == "dungeon":
            play_dungeon()
        elif location == "bedroom":
            play_bedroom()
        elif location == "battlements":
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


newspaper = Newspaper()


class Torch:
    """Torches help to shed light in the darkness."""

    def __repr__(self):
        return "It's a flaming torch.\n"

    def __str__(self):
        return "torch"


torch = Torch()


class FrontDoor:
    """You could use the front door to enter the castle."""

    def __repr__(self):
        return "The front door of the castle.\n"

    def __str__(self):
        return "door"


front_door = FrontDoor()


class HelpFunction:
    def __repr__(self):
        return function_repr_template.format(name="help")

    def __call__(self, *args):
        if len(args) == 0:
            self._tutorial()
        elif len(args) == 1:
            arg = args[0]
            speak(arg.__doc__)
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
    def __repr__(self):
        return function_repr_template.format(name="take")

    def __call__(self, *args):
        if len(args) == 0:
            speak("Did you mean to take something?")
        for o in args:
            self._take(o)

    def _take(self, o):
        location = game_state["location"]
        available = game_state[location]
        holding = game_state["holding"]

        if o in holding:
            speak(f"You are alreading holding the {ANSI.BOLD}{o}{ANSI.RESET}.")
        elif o not in available:
            speak(f"The {ANSI.BOLD}{o}{ANSI.RESET} is not available.")
        elif o in fixed:
            speak(f"The {ANSI.BOLD}{o}{ANSI.RESET} cannot be taken.")
        else:
            available.remove(o)
            holding.add(o)
            speak(f"You have taken the {ANSI.BOLD}{o}{ANSI.RESET}.")
            output()
            status()
        output()


help = HelpFunction()
take = TakeFunction()


game_state = {
    "location": "outside",
    "outside": {newspaper, torch, front_door},
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
    speak(f"Objects available: [{ANSI.BOLD}{available_str}{ANSI.RESET}]")
    speak(f"Objects held: [{ANSI.BOLD}{holding_str}{ANSI.RESET}]")

    namespace = dict()
    for o in available:
        namespace[str(o)] = o
    for o in holding:
        namespace[str(o)] = o
    namespace["help"] = help
    namespace["take"] = take
    # TODO use
    # TODO sing
    return namespace


def play_outside():
    output()
    speak("You are standing outside a castle.")
    output()
    namespace = status()
    output()

    try:
        code.interact(local=namespace, banner="")
    except InteractionComplete:
        pass


def play_hall():
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
