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


loading_node = get_element_by_id("loading")
play_button_node = get_element_by_id("play_button")
prologue_node = get_element_by_id("prologue")
screen_node = get_element_by_id("screen")
terminal = get_terminal()


class Game:
    def __init__(self):
        self.location = outside
        self.game_over = False

    def play(self):
        pass


class BreakInteraction(SystemExit):
    pass


class Location:
    def __init__(self):
        self.objects = set()


class Outside(Location):
    def __init__(self):
        self.objects.add(door)
        self.objects.add(torch)
        self.objects.add(newspaper)

    def play(self):
        pass


outside = Outside()

Location = Enum("Location", ["OUTSIDE", "HALL", "DUNGEON", "BEDROOM", "BATTLEMENTS"])


def play():
    hide(prologue_node)
    screen_node.style.visibility = "visible"

    #     write(f"\n{ANSI.BOLD}")
    #     speak("   || The Scottish play")
    #     speak(f"===||====={ANSI.BG_RED}=====>>>{ANSI.RESET}")
    #     speak(f"{ANSI.BOLD}   ||")
    #     write(f"{ANSI.RESET}\n")
    #     speak(
    #         f"""\
    # Type {ANSI.BOLD}help(){ANSI.RESET} for the in-game tutorial.
    # ---"""
    #     )

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

    game_over()


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


class FlamingTorch:
    """Torches help to shed light in the darkness."""

    def __repr__(self):
        return "It's a flaming torch.\n"

    def __str__(self):
        return "torch"

    def use(self):
        location = game_state["location"]
        if location == Location.HALL:
            assert not game_state["hall_lit"]
            # TODO output?
            game_state["hall_lit"] = True
            game_state["holding"].remove(self)
            game_state[location].add(stairs)
            game_state[location].add(tunnel)
            game_state[location].add(log)
            raise BreakInteraction
        else:
            output("No point using the torch here, it's nice and light already.")
            output()


class FrontDoor:
    """You could use the front door to enter the castle."""

    def __repr__(self):
        return "The front door of the castle.\n"

    def __str__(self):
        return "door"

    def use(self):
        location = game_state["location"]
        assert location in {Location.OUTSIDE, Location.HALL}
        if location == Location.OUTSIDE:
            game_state["location"] = Location.HALL
        else:
            game_state["location"] = Location.OUTSIDE
        raise BreakInteraction


class Stairs:
    """You could see what's upstairs."""

    def __repr__(self):
        return "TODO A spiral stone staircase.\n"

    def __str__(self):
        return "stairs"

    def use(self):
        location = game_state["location"]
        assert location in {Location.HALL, Location.BEDROOM}
        if location == Location.HALL:
            game_state["location"] = Location.BEDROOM
        else:
            game_state["location"] = Location.HALL
        raise BreakInteraction


class Tunnel:
    """You could use the tunnel to find out what's below the castle."""

    def __repr__(self):
        return "TODO A dark and smelly tunnel.\n"

    def __str__(self):
        return "tunnel"

    def use(self):
        location = game_state["location"]
        assert location in {Location.HALL, Location.DUNGEON}
        if location == Location.HALL:
            game_state["location"] = Location.DUNGEON
        else:
            game_state["location"] = Location.HALL
        raise BreakInteraction


class WoodenLog:
    """TODO help."""

    def __repr__(self):
        return "TODO a wooden log.\n"

    def __str__(self):
        return "log"

    def use(self):
        location = game_state["location"]
        if location == Location.DUNGEON:
            assert not game_state["prophecy_heard"]
            game_state["holding"].remove(self)
            output("TODO prophecy")
            output()
            game_state["prophecy_heard"] = True
            game_state[Location.HALL].add(dagger)
            raise BreakInteraction
        else:
            output("TODO not very useful here.")
            output()


class BedroomWindow:
    """You could use the window to get out onto the battlements."""

    def __repr__(self):
        return "The bedroom window.\n"

    def __str__(self):
        return "window"

    def use(self):
        location = game_state["location"]
        assert location in {Location.BEDROOM, Location.BATTLEMENTS}
        if location == Location.BEDROOM:
            game_state["location"] = Location.BATTLEMENTS
        else:
            game_state["location"] = Location.BEDROOM
        raise BreakInteraction


class Dagger:
    """TODO help."""

    def __repr__(self):
        return "TODO a dagger.\n"

    def __str__(self):
        return "dagger"

    def use(self):
        location = game_state["location"]
        if location == Location.BEDROOM:
            assert not computer.destroyed
            output("TODO you used the dagger")
            computer.destroyed = True
            game_state["holding"].remove(dagger)
            game_state[Location.BEDROOM].add(crown)
            output()
        else:
            output("TODO can't use that here")
            output()


class Computer:
    """TODO help."""

    def __init__(self):
        self.destroyed = False

    def __repr__(self):
        if self.destroyed:
            return "TODO a destroyed computer.\n"
        else:
            return "TODO a computer.\n"

    def __str__(self):
        return "computer"

    def use(self):
        if self.destroyed:
            output("TODO can't use computer, it's destroyed")
        else:
            output("TODO use the computer.")


class Crown:
    """TODO help."""

    def __init__(self):
        self.used = False

    def __repr__(self):
        return "TODO a crown.\n"

    def __str__(self):
        return "crown"

    def use(self):
        location = game_state["location"]
        if location == Location.BATTLEMENTS:
            assert not self.used
            self.used = True
            game_state["holding"].remove(crown)
            output("TODO you used the crown")
            output()
        else:
            output("TODO can't use that here")
            output()


class Telescope:
    """TODO help."""

    def __repr__(self):
        return "TODO a telescope.\n"

    def __str__(self):
        return "telescope"

    def use(self):
        pass


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
            output_object_status()
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
        location = game_state["location"]
        if location == Location.BATTLEMENTS:
            speak(
                f"""{ANSI.ITALICIZE}\
I'm a lumberjack, and I'm okay
I sleep all night and I work all day
I cut down trees, I eat my lunch
I go to the lavatory
On Wednesdays I go shoppin'
And have buttered scones for tea.{ANSI.RESET}
"""
            )
            if crown.used:
                output("TODO forest runs away, you win!")
                game_state["forest_defeated"] = True
                game_state["game_over"] = True
                raise BreakInteraction
        else:
            # TODO sing causes death
            output("TODO sing")
            game_state["game_over"] = True
            raise BreakInteraction


newspaper = Newspaper()
torch = FlamingTorch()
door = FrontDoor()
stairs = Stairs()
tunnel = Tunnel()
window = BedroomWindow()
log = WoodenLog()
dagger = Dagger()
computer = Computer()
telescope = Telescope()
crown = Crown()
help = HelpFunction()
take = TakeFunction()
use = UseFunction()
sing = SingFunction()


# Initial game state.
game_state = {
    "location": Location.OUTSIDE,
    Location.OUTSIDE: {newspaper, torch, door},
    Location.HALL: {door},
    Location.DUNGEON: {tunnel},
    Location.BEDROOM: {stairs, window, computer},
    Location.BATTLEMENTS: {window, telescope},
    "holding": set(),
    "hall_lit": False,
    "prophecy_heard": False,
    "forest_defeated": False,
    "game_over": False,
}


# These objects cannot be taken.
fixed = {door, tunnel, stairs, window, telescope, computer}


def output_object_status():
    location = game_state["location"]
    available = game_state[location]
    holding = game_state["holding"]
    available_str = ", ".join([str(o) for o in available])
    holding_str = ", ".join([str(o) for o in holding])
    output(f"Objects available: [{ANSI.BOLD}{available_str}{ANSI.RESET}]", 0)
    output(f"Objects held: [{ANSI.BOLD}{holding_str}{ANSI.RESET}]", 1)


def setup_namespace():
    location = game_state["location"]
    available = game_state[location]
    holding = game_state["holding"]
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
    output("You are standing outside the king's castle.", 1)
    output()
    output_object_status()
    output()

    namespace = setup_namespace()
    try:
        code.interact(local=namespace, banner="")
    except BreakInteraction:
        pass


def play_hall():
    hall_lit = game_state["hall_lit"]
    if hall_lit:
        play_hall_lit()
    else:
        play_hall_dark()


def play_hall_dark():
    output()
    output("You are in the main hall. It's very dark in here.", 1)
    output()
    output_object_status()
    output()

    namespace = setup_namespace()
    try:
        code.interact(local=namespace, banner="")
    except BreakInteraction:
        pass


def play_hall_lit():
    output()
    if dagger in game_state[Location.HALL]:
        speak(
            f"""{ANSI.ITALICIZE}\
Is this a dagger which I see before me,
The handle toward my hand? Come, let me clutch thee.
I have thee not, and yet I see thee still.{ANSI.RESET}"""
        )
        output()
    output("You are in the main hall. It's nice and light in here.", 1)
    output("There's are stairs going up and a tunnel going down.", 1)
    output()
    output_object_status()
    output()

    namespace = setup_namespace()
    try:
        code.interact(local=namespace, banner="")
    except BreakInteraction:
        pass


def play_dungeon():
    prophecy_heard = game_state["prophecy_heard"]
    if prophecy_heard:
        play_dungeon_no_witches()
    else:
        play_dungeon_witches()


def play_dungeon_witches():
    output()
    output("You are in the dungeon.", 1)
    output("There are three witches. They don't look very happy.", 1)
    output("The fire under their cauldron is burning out.", 1)
    output()
    output_object_status()
    output()

    namespace = setup_namespace()
    try:
        code.interact(local=namespace, banner="")
    except BreakInteraction:
        pass


def play_dungeon_no_witches():
    output()
    output("You are in the dungeon. The witches are gone.", 1)
    output()
    output_object_status()
    output()

    namespace = setup_namespace()
    try:
        code.interact(local=namespace, banner="")
    except BreakInteraction:
        pass


def play_bedroom():
    output()
    output("You are in the king's bedroom.", 1)
    output()
    output_object_status()
    output()

    namespace = setup_namespace()
    try:
        code.interact(local=namespace, banner="")
    except BreakInteraction:
        pass


def play_battlements():
    output()
    output("You are on the castle battlements.", 1)
    if crown.used:
        output("TODO an army of trees is attacking! You won't be king for long.")
    output()
    output_object_status()
    output()

    namespace = setup_namespace()
    try:
        code.interact(local=namespace, banner="")
    except BreakInteraction:
        pass


def game_over():
    pass


@when("click", "#play_button")
def play_button_on_click(event):
    play()


if __name__ == "__main__":
    hide(loading_node)
    show(play_button_node)
    play()
