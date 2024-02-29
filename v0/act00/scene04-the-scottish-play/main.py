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
        self.over = False

    def play(self):
        hide(prologue_node)
        screen_node.style.visibility = "visible"

        write(f"\n{ANSI.BOLD}")
        speak("   || The Scottish play")
        speak(f"===||====={ANSI.BG_RED}=====>>>{ANSI.RESET}")
        speak(f"{ANSI.BOLD}   ||")
        write(f"{ANSI.RESET}\n")
        speak(
            f"""\
Type {ANSI.BOLD}help(){ANSI.RESET} for the in-game tutorial.
---"""
        )

        while not self.over:
            player.location.play()

        output_game_over()


def output_game_over():
    output("TODO GAME OVER")


def output_objects():
    available = player.location.objects
    taken = player.objects
    available_str = ", ".join([str(o) for o in available])
    taken_str = ", ".join([str(o) for o in taken])
    output(f"Objects available: [{ANSI.BOLD}{available_str}{ANSI.RESET}]", 0)
    output(f"Objects taken: [{ANSI.BOLD}{taken_str}{ANSI.RESET}]", 1)


def setup_namespace():
    namespace = dict()

    # Add objects.
    for o in player.objects:
        namespace[str(o)] = o
    for o in player.location.objects:
        namespace[str(o)] = o

    # Add action functions.
    namespace["help"] = help
    namespace["take"] = take
    namespace["use"] = use
    namespace["sing"] = sing

    return namespace


class Player:
    def __init__(self):
        self.location = outside
        self.objects = set()

    def sing(self):
        if self.location is battlements:
            speak(
                f"""
{ANSI.ITALICIZE}I'm a lumberjack, and I'm okay.
I sleep all night and I work all day.
I cut down trees, I eat my lunch,
I go to the lavatory.
On Wednesdays I go shoppin',
And have buttered scones for tea.{ANSI.RESET}
"""
            )
            if crown.used:
                output("TODO forest runs away, you win!")
                game.forest = False
                game.over = True
                raise BreakInteraction
        else:
            output("TODO singing causes death")
            game.over = True
            raise BreakInteraction


class Forest:
    def __init__(self):
        self.defeated = False


forest = Forest()


class BreakInteraction(SystemExit):
    """This exception is used to signal that the game state has
    changed and that the current interactive session should be
    interrupted."""

    pass


class Location:
    def __init__(self):
        self.objects = set()


class Outside(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(door)
        self.objects.add(torch)
        self.objects.add(newspaper)

    def play(self):
        output()
        output("You are standing outside the king's castle.", 1)
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except BreakInteraction:
            pass


class Hall(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(door)
        self.dark = True

    def play(self):
        if self.dark:
            self.play_dark()
        else:
            self.play_light()

    def play_dark(self):
        output()
        output("You are in the main hall. It's very dark in here.", 1)
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except BreakInteraction:
            pass

    def play_light(self):
        output()
        output("You are in the main hall. It's nice and light in here.", 1)
        output("There's are stairs going up and a tunnel going down.", 1)
        output()
        output_objects()
        output()

        if dagger in self.objects:
            speak(
                f"""{ANSI.ITALICIZE}\
Is this a dagger which I see before me,
The handle toward my hand? Come, let me clutch thee.
I have thee not, and yet I see thee still.{ANSI.RESET}"""
            )
            output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except BreakInteraction:
            pass


class Dungeon(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(tunnel)
        self.witches = True

    def play(self):
        if self.witches:
            self.play_witches()
        else:
            self.play_no_witches()

    def play_witches(self):
        output()
        output("You are in the dungeon.", 1)
        output("There are three witches. They don't look very happy.", 1)
        output("The fire under their cauldron is burning out.", 1)
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except BreakInteraction:
            pass

    def play_no_witches(self):
        output()
        output("You are in the dungeon. The witches are gone.", 1)
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except BreakInteraction:
            pass


class Bedroom(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(stairs)
        self.objects.add(window)
        self.objects.add(computer)

    def play(self):
        output()
        output("You are in the king's bedroom.", 1)
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except BreakInteraction:
            pass


class Battlements(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(window)
        self.objects.add(telescope)

    def play(self):
        output()
        output("You are on the castle battlements.", 1)
        if crown.used:
            output("TODO an army of trees is attacking! You won't be king for long.")
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except BreakInteraction:
            pass


class Usable:
    pass


class Takeable:
    pass


class Newspaper(Usable, Takeable):
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

Led by Macbeth, his greatest captain, King Dunguido's army dealt a decisive blow and ended the revolt.

A sergeant in the King's army said:

{ANSI.ITALICIZE}For brave Macbeth (well he deserves that name),
Disdaining Fortune, with his brandished steel,
Which smoked with bloody execution,
Like Valor's minion, carved out his passage
Till he faced the slave;
Which ne'er shook hands, nor bade farewell to him,
Till he unseamed him from the nave to th' chops,
And fixed his head upon our battlements.{ANSI.RESET}

Macbeth is on his way to the King's castle to celebrate the victory.
"""
        )


class Torch(Usable, Takeable):
    """Torches help to shed light in the darkness."""

    def __repr__(self):
        return "It's a flaming torch.\n"

    def __str__(self):
        return "torch"

    def use(self):
        if player.location is hall:
            assert hall.dark
            # TODO output?
            hall.dark = False
            player.objects.remove(self)
            hall.objects.add(stairs)
            hall.objects.add(tunnel)
            hall.objects.add(log)
            raise BreakInteraction
        else:
            output("No point using the torch here, it's nice and light already.")
            output()


class Door(Usable):
    """You could use the front door to enter the castle."""

    def __repr__(self):
        return "The front door of the castle.\n"

    def __str__(self):
        return "door"

    def use(self):
        location = player.location
        assert location in {outside, hall}
        if location is outside:
            player.location = hall
        else:
            player.location = outside
        raise BreakInteraction


class Stairs(Usable):
    """You could see what's upstairs."""

    def __repr__(self):
        return "TODO A spiral stone staircase.\n"

    def __str__(self):
        return "stairs"

    def use(self):
        location = player.location
        assert location in {hall, bedroom}
        if location is hall:
            player.location = bedroom
        else:
            player.location = hall
        raise BreakInteraction


class Tunnel(Usable):
    """You could use the tunnel to find out what's below the castle."""

    def __repr__(self):
        return "TODO A dark and smelly tunnel.\n"

    def __str__(self):
        return "tunnel"

    def use(self):
        location = player.location
        assert location in {hall, dungeon}
        if location is hall:
            player.location = dungeon
        else:
            player.location = hall
        raise BreakInteraction


class Log(Usable, Takeable):
    """TODO help."""

    def __repr__(self):
        return "TODO a wooden log.\n"

    def __str__(self):
        return "log"

    def use(self):
        location = player.location
        if location is dungeon:
            assert dungeon.witches
            player.objects.remove(self)
            output("TODO prophecy")
            output()
            dungeon.witches = False
            hall.objects.add(dagger)
            raise BreakInteraction
        else:
            output("TODO not very useful here.")
            output()


class Window(Usable):
    """You could use the window to get out onto the battlements."""

    def __repr__(self):
        return "The bedroom window.\n"

    def __str__(self):
        return "window"

    def use(self):
        location = player.location
        assert location in {bedroom, battlements}
        if location is bedroom:
            player.location = battlements
        else:
            player.location = bedroom
        raise BreakInteraction


class Dagger(Usable, Takeable):
    """TODO help."""

    def __repr__(self):
        return "TODO a dagger.\n"

    def __str__(self):
        return "dagger"

    def use(self):
        location = player.location
        if location is bedroom:
            assert not computer.destroyed
            computer.destroyed = True
            player.objects.remove(dagger)
            bedroom.objects.add(crown)
            output("TODO you used the dagger")
            output()
            raise BreakInteraction
        else:
            output("TODO can't use that here")
            output()


class Computer(Usable):
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


class Crown(Usable, Takeable):
    """TODO help."""

    def __init__(self):
        self.used = False

    def __repr__(self):
        return "TODO a crown.\n"

    def __str__(self):
        return "crown"

    def use(self):
        location = player.location
        if location is battlements:
            assert not self.used
            self.used = True
            player.objects.remove(crown)
            output("TODO you used the crown")
            output()
        else:
            output("TODO can't use that here")
            output()


class Telescope(Usable):
    """TODO help."""

    def __repr__(self):
        return "TODO a telescope.\n"

    def __str__(self):
        return "telescope"

    def use(self):
        pass


class Action:
    pass


class Help(Action):
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
In each location you will find some objects. These objects can be used to help you on your quest for ultimate power and glory.

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


class Take(Action):
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
        available = player.location.objects
        taken = player.objects

        if o in taken:
            output(f"You have already taken the {o}.")
        elif o not in available:
            output(f"The {o} is not available.")
        elif not isinstance(o, Takeable):
            output(f"The {o} cannot be taken.")
        else:
            available.remove(o)
            taken.add(o)
            output(f"You have taken the {o}.", 1)
            output()
            output_objects()
        output()


class Use(Action):
    """Type use(X) to try and use object X."""

    def __repr__(self):
        return function_repr_template.format(name="use") + "\n"

    def __call__(self, *args):
        if len(args) == 0:
            output("Did you mean to use something?")
            output()
        for o in args:
            if isinstance(o, Usable):
                o.use()
            else:
                output(f"Object {o} cannot be used.")


class Sing(Action):
    """Type sing() any time you feel like singing!"""

    def __repr__(self):
        return function_repr_template.format(name="sing") + "\n"

    def __call__(self, *args):
        player.sing()


# Objects.
newspaper = Newspaper()
torch = Torch()
door = Door()
stairs = Stairs()
tunnel = Tunnel()
window = Window()
log = Log()
dagger = Dagger()
computer = Computer()
telescope = Telescope()
crown = Crown()

# Locations.
outside = Outside()
hall = Hall()
dungeon = Dungeon()
bedroom = Bedroom()
battlements = Battlements()

# Actions.
help = Help()
take = Take()
use = Use()
sing = Sing()

# Game setup.
player = Player()
game = Game()


@when("click", "#play_button")
def play_button_on_click(event):
    game.play()


if __name__ == "__main__":
    hide(loading_node)
    show(play_button_node)
    game.play()
