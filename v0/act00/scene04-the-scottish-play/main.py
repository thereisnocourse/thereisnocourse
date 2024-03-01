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


class Inspectable(ABC):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = get_wrapper().fill(description)

    def __str__(self):
        return self.name

    def __repr__(self):
        return make_repr(self.description)


class Usable(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def use(self):
        pass


class Takeable(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()


class Game:
    def __init__(self):
        self.over = False

    def play(self):
        hide(prologue_node)
        hide(replay_node)
        screen_node.style.visibility = "visible"

        output()
        speak(f"""\
{Text.BOLD}   || The Scottish play
===||====={Text.BG_RED}=====>>>{Text.RESET}
{Text.BOLD}   ||{Text.RESET}\
""")
        output()
        output(f"Type {Text.BOLD}help(){Text.RESET} for the in-game tutorial.")
        output("---", 1)
        output()

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


def make_repr(s):
    return get_wrapper().fill(s) + "\n"


class Player:
    def __init__(self):
        self.location = outside
        self.objects = set()
        self.crowned = False

    def take(self, o):
        available = self.location.objects
        taken = self.objects

        if o in taken:
            output(f"You've already taken the {o}.")
        elif o not in available or not isinstance(o, Takeable):
            output(f"The {o} cannot be taken.")
        else:
            available.remove(o)
            taken.add(o)
            output(f"You have taken the {o}.")
        output()

    def sing(self):
        if self.location is outside:
            speak(
                f"""\
{Text.ITALICIZE}Do de do do do do
Do de do do do do de 
I'm siiiiingin' in the rain, just siiiiiingin' in the rain⏸
What a gloooooorious feeeeeeeling I'm haaaaaappy again⏸
I'm laaaaaughing at clouds, so daaaaaark up above⏸
The sun's in my heart and I'm ready for⏩

{Text.RESET}{Text.BOLD}[FLASH!]{Text.RESET}"""
            )
            output("", 1)
            output(
                "You've been struck by a bolt of lightning.",
                1,
            )
            game.over = True
            raise SystemExit

        elif self.location is hall:
            speak(
                f"""\
{Text.ITALICIZE}Once, I had an empire in a golden age,
I was held up so high, I used to be great,
They used to cheer when they saw my face,
Now, I fear I have fallen from grace,
And I feel like my castle's crumbling down⏩

{Text.RESET}{Text.BOLD}[CRASH!]{Text.RESET}"""
            )
            output("", 1)
            output(
                "The ceiling has collapsed.",
                1,
            )
            game.over = True
            raise SystemExit

        elif self.location is dungeon:
            speak(
                f"""\
{Text.ITALICIZE}Ding-dong the witch is dead,
Which old witch — the wicked witch!
Ding-dong the wicked witch is dead.
Wake up you sleepyhead,
Rub your eyes, get out of bed,
Wake up the wicked witch is⏩

{Text.RESET}{Text.BOLD}[KAZAM!]{Text.RESET}"""
            )
            output("", 1)
            output("You've been turned into a toad.", 1)
            game.over = True
            raise SystemExit

        elif self.location is bedroom:
            speak(
                f"""\
{Text.ITALICIZE}Het is een nacht
Die je normaal alleen in films ziet
Het is een nacht
Die wordt bezongen in het mooiste lied
Het is een nacht
Waarvan ik dacht dat ik hem nooit beleven zou
Maar vannacht beleef ik hem met jouooooooooOOOOoo⏩

{Text.RESET}{Text.BOLD}[CRUNCH!]{Text.RESET}"""
            )
            output("", 1)
            output(
                "The king has banished you for mangling his favourite song.",
                1,
            )
            game.over = True
            raise SystemExit

        else:
            assert self.location is battlements
            speak(
                f"""\
{Text.ITALICIZE}I'm a lumberjack and I'm okay,
I sleep all night and I work all day.
I cut down trees, I eat my lunch,
I go to the lavatory.
On Wednesdays I go shoppin',
And have buttered scones for tea.{Text.RESET}\
"""
            )
            if player.crowned:
                output()
                speak(
                    """\
The army of trees has throw down their weapons and surrendered! HOORAY!                      

Congratulations! You have nothing more to fear. You shall live a long and happy life, unchallenged as the Most Awesome Programmer in the world!

Who'd have thought this game would have a happy ending, eh? :-)"""
                )
                forest.defeated = True
                game.over = True
                raise SystemExit


class Forest:
    def __init__(self):
        self.defeated = False


forest = Forest()


class Location(Inspectable):
    def __init__(self, name, description):
        super().__init__(name=name, description=description)
        self.objects = set()

    def output_objects(self):
        available = self.objects
        holding = player.objects
        available_str = ", ".join([str(o) for o in available])
        holding_str = ", ".join([str(o) for o in holding])
        output(f"Objects available: [{Text.BOLD}{available_str}{Text.RESET}]")
        output(f"You are holding: [{Text.BOLD}{holding_str}{Text.RESET}]")

    def output_location(self):
        output(
            f"Location: {Text.BOLD}{self.name}{Text.RESET}",
        )

    def output_header(self):
        self.output_location()
        self.output_objects()
        output()
        output(self.description)
        output()

    def setup_namespace(self):
        namespace = dict()

        # Add objects.
        for o in player.objects:
            namespace[str(o)] = o
        for o in self.objects:
            namespace[str(o)] = o

        # Add action functions.
        namespace["help"] = help
        namespace["take"] = take
        namespace["use"] = use
        namespace["sing"] = sing

        # Add current location.
        namespace[self.name] = self

        return namespace

    def interact(self):
        namespace = self.setup_namespace()
        try:
            code.interact(local=namespace, banner="")
        except SystemExit:
            # This exception can be raised to end interaction and
            # return control to the main game loop.
            pass


class Outside(Location):
    def __init__(self):
        super().__init__(
            name="outside",
            description="You are standing outside the king's castle. The weather is awful - thunder, lightning and rain.",
        )
        self.objects.add(door)
        self.objects.add(torch)
        self.objects.add(newspaper)
        self.visited = False

    def play(self):
        self.output_header()
        if not self.visited:
            # Only show this the first time, otherwise gets tedious.
            speak(
                f"{Text.ITALICIZE}So foul and fair a day I have not seen.{Text.RESET}"
            )
            output()
            self.visited = True
        self.interact()


class Hall(Location):
    def __init__(self):
        super().__init__(
            name="hall", description="You are in the main hall. It's very dark here."
        )
        self.objects.add(door)
        self.dark = True

    def play(self):
        self.output_header()
        if self.dark:
            self.play_dark()
        else:
            self.play_light()

    def play_dark(self):
        self.interact()

    def play_light(self):
        if dagger in self.objects:
            speak(
                f"""\
{Text.ITALICIZE}Is this a dagger which I see before me,
The handle toward my hand? Come, let me clutch thee.
I have thee not, and yet I see thee still.{Text.RESET}"""
            )
            output()

        self.interact()


class Dungeon(Location):
    def __init__(self):
        super().__init__(
            name="dungeon",
            description="You are in the dungeon. There are three witches. They don't look very happy. The fire under their cauldron is going out.",
        )
        self.objects.add(tunnel)
        self.witches = True

    def play(self):
        self.output_header()
        self.interact()


class Bedroom(Location):
    def __init__(self):
        super().__init__(
            name="bedroom",
            description="You are in the king's bedroom. King Dunguido Macrossum is asleep on the bed. His computer is on, it looks like he was playing a game.",
        )
        self.objects.add(stairs)
        self.objects.add(window)
        self.objects.add(computer)

    def play(self):
        self.output_header()
        self.interact()


class Battlements(Location):
    def __init__(self):
        super().__init__(
            name="battlements", description="You are on the castle battlements."
        )
        self.objects.add(window)
        self.objects.add(telescope)

    def play(self):
        self.output_header()
        self.interact()


class Newspaper(Inspectable, Usable, Takeable):
    """You can use newspapers to learn more about current affairs."""

    def __init__(self):
        super().__init__(
            name="newspaper",
            description="Today's newspaper. The story on the front page looks interesting.",
        )

    def use(self):
        # There are no preconditions, the newspaper can be used at
        # any time in the game.
        speak(
            f"""\
14 August 1040

{Text.BOLD}MACDONWALD DEFEATED{Text.RESET}

Dunguido Macrossum, King of Scotland, has defeated the rebel Macdonwald of the Western Isles.

Led by Macbeth, his greatest captain, King Dunguido's army dealt a decisive blow and ended the revolt.

A sergeant in the King's army said:

{Text.ITALICIZE}For brave Macbeth (well he deserves that name),
Disdaining Fortune, with his brandished steel,
Which smoked with bloody execution,
Like Valor's minion, carved out his passage
Till he faced the slave;
Which ne'er shook hands, nor bade farewell to him,
Till he unseamed him from the nave to th' chops,
And fixed his head upon our battlements.{Text.RESET}

Macbeth now travels to the King's castle to celebrate the victory.
"""
        )
        output()


class Torch(Inspectable, Usable, Takeable):
    """Torches can be used to provide light in the darkness."""

    def __init__(self):
        super().__init__(name="torch", description="A flaming torch.")

    def use(self):
        if player.location is hall:
            assert hall.dark
            speak("Good idea! You use the torch to find some candles and light them...")
            hall.dark = False
            hall.description = "It's nice and light here now. There are stairs going up and a tunnel going down."
            player.objects.remove(self)
            hall.objects.add(stairs)
            hall.objects.add(tunnel)
            hall.objects.add(log)
            raise SystemExit
        else:
            output("No point using the torch here, it's nice and light already.")
            output()


class Door(Inspectable, Usable):
    """You could use the front door to enter the castle."""

    def __init__(self):
        super().__init__(name="door", description="The front door of the castle.")

    def use(self):
        location = player.location
        assert location in {outside, hall}
        if location is outside:
            speak("You step into the castle...")
            player.location = hall
        else:
            speak("You go back outside into the rain...")
            player.location = outside
        raise SystemExit


class Stairs(Inspectable, Usable):
    """You could use the stairs to visit the king's bedroom."""

    def __init__(self):
        super().__init__(
            name="stairs",
            description="A spiral staircase between the hall and the king's bedroom.",
        )

    def use(self):
        location = player.location
        assert location in {hall, bedroom}
        if location is hall:
            speak("You climb up the stairs...")
            player.location = bedroom
        else:
            speak("You climb back down the stairs...")
            player.location = hall
        raise SystemExit


class Tunnel(Inspectable, Usable):
    """You could use the tunnel to find out what's below the castle."""

    def __init__(self):
        super().__init__(
            name="tunnel",
            description="A dark, mysterious and slightly smelly tunnel between the hall and the dungeons.",
        )

    def use(self):
        location = player.location
        assert location in {hall, dungeon}
        if location is hall:
            speak("You walk down into the darkness...")
            player.location = dungeon
        else:
            speak("You walk back up towards the light...")
            player.location = hall
        raise SystemExit


class Log(Inspectable, Usable, Takeable):
    """You could use the log to stoke a fire."""

    def __init__(self):
        super().__init__(name="log", description="A wooden log, nice and dry.")

    def use(self):
        location = player.location
        if location is dungeon:
            assert dungeon.witches
            player.objects.remove(self)
            speak(
                f"""\
{Text.ITALICIZE}Fillet of a fenny snake
In the cauldron boil and bake.
Eye of newt and toe of frog,
Wool of bat and tongue of dog,
Adder's fork and blindworm's sting,
Lizard's leg and howlet's wing,
For a charm of powerful trouble,
Like a hell-broth boil and bubble.{Text.RESET}

Through the mystical and pungent haze above their cauldron, the witches look at you and say:

{Text.ITALICIZE}All hail, Macbeth, that shalt be king hereafter!{Text.RESET}

Then into thin air, the witches vanish!
"""
            )
            dungeon.witches = False
            dungeon.description = "The witches are gone."
            hall.objects.add(dagger)
            raise SystemExit
        else:
            output("There's no fire here.")
            output()


class Window(Inspectable, Usable):
    """You could use the window to get out onto the battlements."""

    def __init__(self):
        super().__init__(
            name="window",
            description="The bedroom window. It looks out onto the battlements.",
        )

    def use(self):
        location = player.location
        assert location in {bedroom, battlements}
        if location is bedroom:
            speak("You climb out onto the castle battlements...")
            player.location = battlements
        else:
            speak("You climb back into the king's bedroom...")
            player.location = bedroom
        raise SystemExit


class Dagger(Inspectable, Usable, Takeable):
    """You could use this dagger to become more powerful!"""

    def __init__(self):
        super().__init__(
            name="dagger",
            description="A dagger. Very pointy. Much more dangerous than fruit.",
        )

    def use(self):
        if player.location is bedroom:
            assert not computer.destroyed
            computer.destroyed = True
            computer.description = "A broken computer."
            player.objects.remove(dagger)
            bedroom.objects.add(crown)
            bedroom.description = "The king has gone."
            speak(
                f"""\
You raise the dagger above your head and...
                  
{Text.BOLD}[CRUNCH]{Text.RESET}

You have destroyed the king's computer! The king awakes and sees the time has come to pass his knowledge and power to another. He takes off his crown and leaves the castle, never to be seen again.
"""
            )
            raise SystemExit
        else:
            output("You can't use the dagger here.")
            output()


# Computer is a special game-within-a-game, behaves like an
# object and a playable location.
class Computer(Location, Usable):
    """Computers are useful for all kinds of things. But mostly for playing games."""

    def __init__(self):
        super().__init__(
            name="computer",
            description="An old computer. It looks like it's still working though.",
        )
        self.destroyed = False

    def use(self):
        if self.destroyed:
            output("You can't use the computer any more, it's broken.")
            output()
        else:
            speak("You sit down at the computer. It looks ancient...")
            player.location = self
            raise SystemExit

    def play(self):
        terminal.clear()
        screen_node.classList.remove("scottish")
        screen_node.classList.add("old_computer")

        self.interact()

        screen_node.classList.add("scottish")
        screen_node.classList.remove("old_computer")
        player.location = bedroom


class Crown(Inspectable, Usable, Takeable):
    """The crown feels like it's brimming with magical powers. Who knows what would happen if you used it!"""

    def __init__(self):
        super().__init__(
            name="crown",
            description="The king's crown. It's engraved with a picture of a snake and the letters \"BDFL\", whatever that means.",
        )

    def use(self):
        if player.location is battlements:
            assert not player.crowned
            speak(
                f"""\
You place the crown upon your head.
It begins to glow immediately.
You feel knowledge and power rushing into your veins.
Fireworks appear and a great fanfare sounds!

CONGRATULATIONS!

You have become the ruler of Scotland and the Most Awesome Programmer in the world!
All hail King Macbeth!

But wait, a messenger arrives:

{Text.ITALICIZE}As I did stand my watch upon the hill,
I looked toward Birnam, and anon methought
The Wood began to move.{Text.RESET}

An army of trees is approaching!
I fear your rule will not last long...
"""
            )
            player.objects.remove(crown)
            player.crowned = True
            battlements.description = "An army of trees is attacking!"
            raise SystemExit
        else:
            output(
                "The crown feels very powerful, best to use it where everyone can see you."
            )
            output()


class Telescope(Inspectable, Usable):
    """You could use the telescope to see what's beyond the battlements."""

    def __init__(self):
        super().__init__(name="telescope", description="An old-fashioned telescope.")

    def use(self):
        if player.crowned:
            speak(
                f"""\
You can see an army of trees approaching!
                  
{Text.ITALICIZE}...and now a wood
Comes toward Dunsinane. Arm, arm, and out!
If this which he avouches does appear,
There is nor flying hence nor tarrying here.{Text.RESET}
"""
            )
        else:
            speak(
                f"""\
You can see some trees in the distance. 

{Text.ITALICIZE}Be lion-mettled, proud, and take no care
Who chafes, who frets, or where conspirers are.
Macbeth shall never vanquished be until
Great Birnam Wood to high Dunsinane Hill
Shall come against him.{Text.RESET}

Who said that?
"""
            )
        output()


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
In each location you will find some objects. These objects can be used to help you on your quest for ultimate power and knowledge.

To look at an object, type the name of the object and press return. For example, to look at the {Text.BOLD}newspaper{Text.RESET}:⏩
              
>>> ⏵⏸newspaper
              
To get help on how to use an object, type {Text.BOLD}help(X){Text.RESET} where {Text.BOLD}X{Text.RESET} is the name of an object. For example:⏩
              
>>> ⏵⏸help(newspaper)

To use an object, type {Text.BOLD}use(X){Text.RESET} where {Text.BOLD}X{Text.RESET} is the name of an object. For example:⏩
              
>>> ⏵⏸use(newspaper)

To take an object and carry it with you to the next location, type {Text.BOLD}take(X){Text.RESET} where {Text.BOLD}X{Text.RESET} is the name of an object. For example:⏩

>>> ⏵⏸take(newspaper)
              
At any point in the game you can {Text.BOLD}sing(){Text.RESET} if you feel like it.

{Text.ITALICIZE}But screw your courage to the sticking place
And we'll not fail!{Text.RESET}
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
                output(f"The {o} cannot be used.")
                output()


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
