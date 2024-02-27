from util import (
    when,
    get_element_by_id,
    show,
    hide,
    write,
    output,
    output_help,
    get_terminal,
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

    write(
        f"""{ANSI.BOLD}
   || The Scottish Play
===||===================>>
   ||
{ANSI.RESET}
"""
    )
    output(
        f"Type {ANSI.BOLD}help(){ANSI.RESET} for more information on how to play the game."
    )
    output("---")

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
        return "It's today's newspaper."

    def __str__(self):
        return "newspaper"


newspaper = Newspaper()


class Torch:
    """Torches help to shed light in the darkness."""

    def __repr__(self):
        return "It's a flaming torch."

    def __str__(self):
        return "torch"


torch = Torch()


class FrontDoor:
    """You could use the front door to enter the castle."""

    def __repr__(self):
        return "The front door of the castle."

    def __str__(self):
        return "door"


front_door = FrontDoor()


class HelpFunction:
    def __repr__(self):
        return function_repr_template.format(name="help")

    def __call__(self, *args):
        if len(args) == 0:
            self.help()
        elif len(args) == 1:
            arg = args[0]
            output(arg.__doc__)

    def help(self):
        output_help(
            [
                """\
In each location you will find some objects. Some will be useful and
help you on your quest.
""",
                f"""\
To look at an object, type the name of the object and press return. E.g.,
to look at the newspaper, type {ANSI.BOLD}newspaper{ANSI.RESET}.
""",
                f"""\
To get help on how to use an object, type {ANSI.BOLD}help(X){ANSI.RESET}
where {ANSI.BOLD}X{ANSI.RESET} is the name of an object. E.g., type
{ANSI.BOLD}help(newspaper){ANSI.RESET}.
""",
                f"""\
To use an object, type {ANSI.BOLD}use(X){ANSI.RESET} where
{ANSI.BOLD}X{ANSI.RESET} is the name of an object. E.g., type
{ANSI.BOLD}use(newspaper){ANSI.RESET}.
""",
                f"""\
To take an object and carry it with you to the next location, type
{ANSI.BOLD}take(X){ANSI.RESET} where {ANSI.BOLD}X{ANSI.RESET} is the
name of an object. E.g., type {ANSI.BOLD}take(newspaper){ANSI.RESET}.
""",
                f"""\
At any point in the game you can {ANSI.BOLD}sing(){ANSI.RESET} if
you feel like it.
""",
            ]
        )


help = HelpFunction()


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
    output(f"Objects available: {ANSI.BOLD}{available_str}{ANSI.RESET}")
    output(f"Objects held: {ANSI.BOLD}{holding_str}{ANSI.RESET}")

    namespace = dict()
    for o in available:
        namespace[str(o)] = o
    for o in holding:
        namespace[str(o)] = o
    namespace["help"] = help
    # TODO take
    # TODO use
    # TODO sing
    return namespace


def play_outside():
    output()
    output(f"{ANSI.UNDERLINE}You are standing outside a castle.{ANSI.RESET}")
    namespace = status()

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
