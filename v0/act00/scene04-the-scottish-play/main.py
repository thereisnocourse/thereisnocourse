from abc import ABC, abstractmethod
import code
from util import (
    when,
    get_element_by_id,
    show,
    hide,
    output,
    get_terminal,
    speak,
    get_wrapper,
    function_repr_template,
    Text,
)


loading_node = get_element_by_id("loading")
play_button_node = get_element_by_id("play_button")
prologue_node = get_element_by_id("prologue")
screen_node = get_element_by_id("screen")
replay_node = get_element_by_id("replay")
success_node = get_element_by_id("success")
terminal = get_terminal()


class Game:
    def __init__(self):
        self.over = False

    def play(self):
        hide(prologue_node)
        hide(replay_node)
        screen_node.style.visibility = "visible"

        # output()
        # speak(f"{Text.BOLD}   || The Scottish play")
        # speak(f"===||====={Text.BG_RED}=====>>>{Text.RESET}")
        # speak(f"{Text.BOLD}   ||{Text.RESET}")
        # output()
        # speak(f'{Text.ITALICIZE}"So foul and fair a day I have not seen."{Text.RESET}')
        # output()
        # speak(f"Type {Text.BOLD}help(){Text.RESET} for the in-game tutorial.")
        # output("---", 1)
        # output()

        while not self.over:
            player.location.play()
            if not self.over:
                terminal.clear()

        output_game_over()


def output_game_over():
    output()
    output(f"{Text.BOLD}GAME OVER{Text.RESET}")
    if forest.defeated:
        show(success_node)
    else:
        show(replay_node)


def output_objects():
    available = player.location.objects
    taken = player.objects
    available_str = ", ".join([str(o) for o in available])
    taken_str = ", ".join([str(o) for o in taken])
    output(f"Objects available: [{Text.BOLD}{available_str}{Text.RESET}]")
    output(f"You are holding: [{Text.BOLD}{taken_str}{Text.RESET}]")


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
        # TODO restore initial location
        # self.location = outside
        self.location = bedroom
        self.objects = set()
        self.crowned = False

    def take(self, o):
        available = self.location.objects
        taken = self.objects

        if o in taken:
            output(f"You've already taken the {o}.")
        elif o not in available:
            output(f"The {o} is not available.")
        elif not isinstance(o, Takeable):
            output(f"The {o} cannot be taken.")
        else:
            available.remove(o)
            taken.add(o)
            output(f"You have taken the {o}.")
            # output()
            # output_objects()
        output()

    def sing(self):
        if self.location is outside:
            output()
            speak(
                f"""\
{Text.ITALICIZE}"Do de do do do do
Do de do do do do de 
I'm siiiiingin' in the rain, just siiiiiingin' in the rain⏸
What a gloooooorious feeeeeeeling I'm haaaaaappy again⏸
I'm laaaaaughing at clouds, so daaaaaark up above⏸
The sun's in my heart and I'm ready for..."
⏩{Text.RESET}{Text.BOLD}[FLASH!]{Text.RESET}"""
            )
            output("", 1)
            output(
                "You've been struck by a bolt of lightning.",
                1,
            )
            game.over = True
            raise SystemExit

        elif self.location is hall:
            output()
            speak(
                f"""\
{Text.ITALICIZE}"Once, I had an empire in a golden age,
I was held up so high, I used to be great,
They used to cheer when they saw my face,
Now, I fear I have fallen from grace,
And I feel like my castle's crumbling down..."
⏩{Text.RESET}{Text.BOLD}[CRASH!]{Text.RESET}"""
            )
            output("", 1)
            output(
                "The ceiling has collapsed.",
                1,
            )
            game.over = True
            raise SystemExit

        elif self.location is dungeon:
            output()
            speak(
                f"""\
{Text.ITALICIZE}"Ding-dong the witch is dead,
Which old witch — the wicked witch!
Ding-dong the wicked witch is dead.
Wake up you sleepyhead,
Rub your eyes, get out of bed,
Wake up the wicked witch is..."
⏩{Text.RESET}{Text.BOLD}[KAZAM!]{Text.RESET}"""
            )
            output("", 1)
            output("The witches have turned you into a toad.", 1)
            game.over = True
            raise SystemExit

        elif self.location is bedroom:
            output()
            speak(
                f"""{Text.ITALICIZE}\
"Het is een nacht
Die je normaal alleen in films ziet
Het is een nacht
Die wordt bezongen in het mooiste lied
Het is een nacht
Waarvan ik dacht dat ik hem nooit beleven zou
Maar vannacht beleef ik hem met jouooooooooOOOOoo..."
⏩{Text.RESET}{Text.BOLD}[CRUNCH!]{Text.RESET}"""
            )
            output("", 1)
            output(
                "The king has mistaken you for an alarm clock and thrown you out of the window.",
                1,
            )
            game.over = True
            raise SystemExit

        else:
            assert self.location is battlements
            output()
            speak(
                f"""{Text.ITALICIZE}\
"I'm a lumberjack and I'm okay,
I sleep all night and I work all day.
I cut down trees, I eat my lunch,
I go to the lavatory.
On Wednesdays I go shoppin',
And have buttered scones for tea."{Text.RESET}\
"""
            )
            if player.crowned:
                output("TODO forest runs away, you win!")
                game.forest = False
                game.over = True
                raise SystemExit


class Forest:
    def __init__(self):
        self.defeated = False


forest = Forest()


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
        output(
            "Location: You are standing outside the king's castle. The weather is awful - thunder, lightning and rain.",
        )
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            pass


class Hall(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(door)
        self.dark = True

    def play(self):
        output("Location: You are in the main hall.")
        if self.dark:
            self.play_dark()
        else:
            self.play_light()

    def play_dark(self):
        output("It's very dark in here.")
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            pass

    def play_light(self):
        output(
            "It's nice and light in here now. There's are stairs going up and a tunnel going down."
        )
        output()
        output_objects()
        output()

        if dagger in self.objects:
            speak(
                f"""{Text.ITALICIZE}\
"Is this a dagger which I see before me,
The handle toward my hand? Come, let me clutch thee.
I have thee not, and yet I see thee still."{Text.RESET}"""
            )
            output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            pass


class Dungeon(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(tunnel)
        self.witches = True

    def play(self):
        output("Location: You are in the dungeon.")
        if self.witches:
            self.play_witches()
        else:
            self.play_no_witches()

    def play_witches(self):
        output(
            "There are three witches. They don't look very happy. The fire under their cauldron is going out."
        )
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            pass

    def play_no_witches(self):
        output("The witches are gone.", 1)
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            pass


class Bedroom(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(stairs)
        self.objects.add(window)
        self.objects.add(computer)

    def play(self):
        output("Location: You are in the king's bedroom.")
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            pass


class Battlements(Location):
    def __init__(self):
        super().__init__()
        self.objects.add(window)
        self.objects.add(telescope)

    def play(self):
        output("Location: You are on the castle battlements.")
        if player.crowned:
            output("TODO an army of trees is attacking! You won't be king for long.")
        output()
        output_objects()
        output()

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            pass


class Usable(ABC):
    @abstractmethod
    def use(self):
        pass


class Takeable(ABC):
    pass


class Newspaper(Usable, Takeable):
    """You can use newspapers to learn more about current affairs."""

    def __repr__(self):
        return (
            get_wrapper().fill(
                "Today's newspaper. The story on the front page looks interesting."
            )
            + "\n"
        )

    def __str__(self):
        return "newspaper"

    def use(self):
        # There are no preconditions, the newspaper can be used at
        # any time in the game.
        output()
        speak(
            f"""\
14 August 1040

{Text.BOLD}MACDONWALD DEFEATED{Text.RESET}

Dunguido Macrossum, King of Scotland, has defeated the rebel Macdonwald of the Western Isles.

Led by Macbeth, his greatest captain, King Dunguido's army dealt a decisive blow and ended the revolt.

A sergeant in the King's army said:

{Text.ITALICIZE}"For brave Macbeth (well he deserves that name),
Disdaining Fortune, with his brandished steel,
Which smoked with bloody execution,
Like Valor's minion, carved out his passage
Till he faced the slave;
Which ne'er shook hands, nor bade farewell to him,
Till he unseamed him from the nave to th' chops,
And fixed his head upon our battlements."{Text.RESET}

Macbeth now travels to the King's castle to celebrate the victory.
"""
        )
        output()


class Torch(Usable, Takeable):
    """Torches can be used to provide light in the darkness."""

    def __repr__(self):
        return get_wrapper().fill("A flaming torch.") + "\n"

    def __str__(self):
        return "torch"

    def use(self):
        if player.location is hall:
            assert hall.dark
            output()
            speak("Good idea! You use the torch to find some candles and light them...")
            hall.dark = False
            player.objects.remove(self)
            hall.objects.add(stairs)
            hall.objects.add(tunnel)
            hall.objects.add(log)
            raise SystemExit
        else:
            output("No point using the torch here, it's nice and light already.")
            output()


class Door(Usable):
    """You could use the front door to enter the castle."""

    def __repr__(self):
        return get_wrapper().fill("The front door of the castle.") + "\n"

    def __str__(self):
        return "door"

    def use(self):
        location = player.location
        assert location in {outside, hall}
        output()
        if location is outside:
            speak("You open the door and step into the castle...")
            player.location = hall
        else:
            speak("You open the door and go back outside into the rain...")
            player.location = outside
        raise SystemExit


class Stairs(Usable):
    """You could use the stairs to visit the king's bedroom."""

    def __repr__(self):
        return (
            get_wrapper().fill(
                "A spiral staircase between the hall and the king's bedroom."
            )
            + "\n"
        )

    def __str__(self):
        return "stairs"

    def use(self):
        location = player.location
        assert location in {hall, bedroom}
        if location is hall:
            player.location = bedroom
        else:
            player.location = hall
        raise SystemExit


class Tunnel(Usable):
    """You could use the tunnel to find out what's below the castle."""

    def __repr__(self):
        return get_wrapper().fill("A dark tunnel.") + "\n"

    def __str__(self):
        return "tunnel"

    def use(self):
        location = player.location
        assert location in {hall, dungeon}
        # TODO output
        if location is hall:
            player.location = dungeon
        else:
            player.location = hall
        raise SystemExit


class Log(Usable, Takeable):
    """You could use the log to stoke a fire."""

    def __repr__(self):
        return get_wrapper().fill("A wooden log, nice and dry.") + "\n"

    def __str__(self):
        return "log"

    def use(self):
        location = player.location
        if location is dungeon:
            assert dungeon.witches
            player.objects.remove(self)
            output()
            speak(
                f"""\
{Text.ITALICIZE}"Fillet of a fenny snake
In the cauldron boil and bake.
Eye of newt and toe of frog,
Wool of bat and tongue of dog,
Adder's fork and blindworm's sting,
Lizard's leg and howlet's wing,
For a charm of powerful trouble,
Like a hell-broth boil and bubble."{Text.RESET}

Looking at you, the witches speak:

{Text.ITALICIZE}"All hail, Macbeth, that shalt be king hereafter!"{Text.RESET}

Then into thin air, the witches vanish...
"""
            )
            dungeon.witches = False
            hall.objects.add(dagger)
            raise SystemExit
        else:
            output("TODO not very useful here.")
            output()


class Window(Usable):
    """You could use the window to get out onto the battlements."""

    def __repr__(self):
        return (
            get_wrapper().fill("The bedroom window. It looks out onto the battlements.")
            + "\n"
        )

    def __str__(self):
        return "window"

    def use(self):
        location = player.location
        assert location in {bedroom, battlements}
        # TODO output
        if location is bedroom:
            player.location = battlements
        else:
            player.location = bedroom
        raise SystemExit


class Dagger(Usable, Takeable):
    """TODO help."""

    def __repr__(self):
        return (
            get_wrapper().fill("A dagger. Very pointy. Much more dangerous than fruit.")
            + "\n"
        )

    def __str__(self):
        return "dagger"

    def use(self):
        if player.location is bedroom:
            assert not computer.destroyed
            computer.destroyed = True
            player.objects.remove(dagger)
            bedroom.objects.add(crown)
            output()
            speak("TODO you used the dagger")
            raise SystemExit
        else:
            output("TODO can't use that here")
            output()


# Computer is a special game-within-a-game, behaves like an
# object and a playable location.
class Computer(Usable, Location):
    """TODO help."""

    def __init__(self):
        super().__init__()
        self.destroyed = False

    def __repr__(self):
        if self.destroyed:
            s = "A broken computer."
        else:
            s = "An old computer. Looks like it's still working though."
        return get_wrapper().fill(s) + "\n"

    def __str__(self):
        return "computer"

    def use(self):
        if self.destroyed:
            output("TODO can't use computer, it's destroyed")
        else:
            output("TODO use the computer.", 2)
            player.location = self
            raise SystemExit

    def play(self):
        terminal.clear()
        screen_node.classList.remove("scottish")
        screen_node.classList.add("old_computer")

        namespace = setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            pass

        screen_node.classList.add("scottish")
        screen_node.classList.remove("old_computer")
        player.location = bedroom


class Crown(Usable, Takeable):
    """TODO help."""

    def __repr__(self):
        return (
            get_wrapper().fill(
                'The king\'s crown. It has the letters "BDFL" engraved in it. Not sure what that means.'
            )
            + "\n"
        )

    def __str__(self):
        return "crown"

    def use(self):
        if player.location is battlements:
            assert not self.used
            player.crowned = True
            player.objects.remove(crown)
            output()
            speak("TODO you used the crown - here come the trees!")
        else:
            output("TODO can't use that here")
            output()


class Telescope(Usable):
    """TODO help."""

    def __repr__(self):
        return get_wrapper().fill("A telescope.") + "\n"

    def __str__(self):
        return "telescope"

    def use(self):
        pass


class Action:
    pass


class Help(Action):
    """Type help() for the in-game tutorial. Type help(X) to get a hint about how to use object X. But then you already knew that :)"""

    def __repr__(self):
        return get_wrapper().fill(function_repr_template.format(name="help")) + "\n"

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

To look at an object, type the name of the object and press return. For example, to look at the {Text.BOLD}newspaper{Text.RESET}:⏩
              
>>> ⏵⏸newspaper
              
To get help on how to use an object, type {Text.BOLD}help(X){Text.RESET} where {Text.BOLD}X{Text.RESET} is the name of an object. For example:⏩
              
>>> ⏵⏸help(newspaper)

To use an object, type {Text.BOLD}use(X){Text.RESET} where {Text.BOLD}X{Text.RESET} is the name of an object. For example:⏩
              
>>> ⏵⏸use(newspaper)

To take an object and carry it with you to the next location, type {Text.BOLD}take(X){Text.RESET} where {Text.BOLD}X{Text.RESET} is the name of an object. For example:⏩

>>> ⏵⏸take(newspaper)
              
At any point in the game you can {Text.BOLD}sing(){Text.RESET} if you feel like it.

"{Text.ITALICIZE}But screw your courage to the sticking place
And we'll not fail!{Text.RESET}"
""",
        )
        output()


class Take(Action):
    """Type take(X) to pick up object X and carry it with you to the next location."""

    def __repr__(self):
        return get_wrapper().fill(function_repr_template.format(name="take")) + "\n"

    def __call__(self, *args):
        if len(args) == 0:
            output("Did you mean to take something?")
            output()
        for o in args:
            player.take(o)


class Use(Action):
    """Type use(X) to try and use object X."""

    def __repr__(self):
        return get_wrapper().fill(function_repr_template.format(name="use")) + "\n"

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
        return get_wrapper().fill(function_repr_template.format(name="sing")) + "\n"

    def __call__(self, *args):
        player.sing()


def init():
    global \
        game, \
        player, \
        newspaper, \
        torch, \
        door, \
        stairs, \
        tunnel, \
        window, \
        log, \
        dagger, \
        computer, \
        telescope, \
        crown, \
        outside, \
        hall, \
        dungeon, \
        bedroom, \
        battlements, \
        help, \
        take, \
        use, \
        sing

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
    init()
    game.play()


@when("click", "#replay_button")
def replay_button_on_click(event):
    terminal.clear()
    init()
    game.play()


if __name__ == "__main__":
    hide(loading_node)
    show(play_button_node)
    init()
    game.play()
