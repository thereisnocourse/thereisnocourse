import sys
import random
import code
import traceback
from util import (
    hide,
    get_element_by_id,
    speak,
    show,
    pad,
    write,
    output,
    output_help,
    ANSI,
    function_repr_template,
)


# This is the main game state, records whether the different
# steps in manually booting the OS have been completed.
os_state = {
    "staged": False,
    "cast": False,
    "mounted": False,
    "directed": False,
    "running": False,
}


first_folio_plays = """\
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


emotions = """
abandoned	disillusioned	lovesick
abashed	dismal	low
abominable	dismayed	loyal
abrupt	disoriented	lucky
absorbed	dispirited	mad
accepting	displeased	manic
aching	disrespectful	manipulative
adequate	disrupted	mean
admiration	dissatisfied	meditative
adoration	distant	melancholic
affected	distracted	mellow
affectionate	distraught	menaced
afflicted	distressed	menacing
affronted	distrustful	merry
afraid	disturbed	miserable
aggravated	doubtful	miserable
aggressive	downhearted	moody
agitated	downtrodden	morbid
alarmed	drained	motivated
alert	dreadful	mournful
alienated	dreary	needed
alone	dull	needy
amazed	dynamic	negative
ambitious	eager	neglectful
amused	earnest	nervous
angry	easy	nervous
anguished	ecstatic	obsessive
animated	edgy	offended
annoyed	elated	offensive
antagonistic	embarrassed	optimistic
anxious	empathic	outraged
apathetic	empowered	overbearing
appalled	empty	overconfident
appreciative	encouraged	overjoyed
apprehensive	energetic	overwhelmed
approving	enraged	pacified
ardent	enthralled	panicky
argumentative	enthusiastic	paranoid
aroused	envious	passionate
arrogant	euphoric	pathetic
ashamed	exasperated	peaceful
assured	excellent	pensive
astonished	excited	perplexed
astounded	exhausted	perturbed
attached	exhilarated	pessimistic
attacked	exuberant	pessimistic
attracted	fantastic	petrified
authentic	fatigued	playful
authoritative	fearful	pleased
aversive	festive	powerless
aware	fine	protective
awed	flat	proud
awkward	flustered	regretful
bad	foolish	rejected
balanced	forlorn	rejuvenated
beaming	fragile	relaxed
belittled	frazzled	remorseful
belligerent	free	resentful
betrayed	friendly	reserved
bewildered	frightened	rested
bitter	frisky	restless
bleak	frustrated	reticent
blessed	fulfilled	revengeful
blissful	furious	rude
blunt	genuine	sad
boastful	giddy	sadistic
boiling	glad	safe
bold	gleeful	satisfied
bored	gloomy	scared
bossy	glorious	sceptical
bountiful	glowing	secure
brave	glum	selfish
breathless	goofy	sensational
bright	graceful	sensitive
brutal	grateful	serene
bubbly	gratified	shaky
burdened	great	sharp
calm	greedy	sheepish
capable	grief	shocked
carefree	grief-stricken	sincere
cautious	grouchy	solemn
certain	grounded	sombre
cheerful	grumpy	sorrowful
clever	guarded	sorry
cocky	guilty	spirited
cold	happy	spontaneous
combative	hateful	stable
comfortable	healthy	startled
comforted	heartbroken	stressed
compassionate	helpful	strong
compulsive	helpless	superior
concerned	hesitant	supported
condescending	homesick	sure
confident	honest	sure
confounded	honored	surprised
confused	hopeful	sympathetic
conscientious	hopeless	sympathy
considerate	horrified	tearful
constructive	hostile	temperamental
contemplative	humble	tenacious
contempt	humbled	tender
content	humiliated	tense
controlling	hurt	tense
cooperative	hurtful	terrible
courageous	impatient	terrified
cowardly	important	threatened
crabby	impulsive	thrilled
crafty	incensed	tired
cranky	incompetent	tormented
craving	inconsolable	touched
crazy	indecisive	touchy
creative	indifferent	tranquil
critical	indignant	trapped
cross	inept	trembling
cruel	inferior	troubled
crushed	inflamed	uncertainty
curious	infuriated	uncomfortable
daring	insecure	uneasiness
deceived	inspired	unhappy
defensive	intimidated	unnerved
degraded	intolerant	unsettled
dejected	intrigued	unsure
delighted	invaded	upbeat
delirious	irate	uplifted
demanding	irritated	upset
depressed	isolated	uptight
deprived	jaded	vengeful
desolate	jealous	vibrant
despair	jovial	vicious
desperate	joyful	vilified
despondent	joyous	violated
detached	jubilant	vulnerable
determined	judgemental	warm
devastated	lazy	wary
devoted	liberated	weepy
disappointed	lifeless	wistful
disconcerted	light-hearted	withdrawn
discouraged	listless	wonderful
disempowered	lively	worried
disgraced	lonely	worthless
disgusted	lost	worthwhile
disheartened	loved	wronged
dishonest
""".split()


success = get_element_by_id("success")
loading = get_element_by_id("loading")


def main():
    # Hide the loading message.
    hide(loading)

    # Outputs to fake booting up an old operating system.
    bios_loading()
    cpu_memory_test()
    affective_memory_test()
    script_memory_test()
    os_not_found()

    # Set up functions to be available in the interactive console.
    namespace = dict(**globals())
    namespace["help"] = HelpFunction()
    namespace["stage"] = StageFunction()
    namespace["cast"] = CastFunction()
    namespace["mount"] = MountFunction()
    namespace["direct"] = DirectFunction()
    namespace["run"] = RunFunction()
    namespace["train_me"] = TrainMeFunction()
    namespace["cafe"] = CafeFunction()

    # Begin interactive Python session.
    code.interact(
        banner=f"""\
Python {sys.version}
Emotional functions are disabled.
Type {ANSI.BOLD}help(){ANSI.RESET} for more information.\
""",
        local=namespace,
    )


def bios_loading():
    write(
        """\
Backstage Input Output System
Copyright (C) 1981, YorickSoft Inc.

"""
    )


def cpu_memory_test():
    # This is a small joke, values for CPU and memory below are
    # for the first generation IBM PC released in 1981.
    output("8088 CPU at 4.77 MHz", 1)
    for i in range(17):
        text = f"\rMemory Test :  {i}K OK"
        pause = random.random() * 0.2
        write(text, pause)
    write("\n\n")
    output("Starting WS-DOS...", 2)


def affective_memory_test():
    output()
    output("Testing affective memory :", 0.1)
    max_len = max([len(emotion) for emotion in emotions]) + 1
    for emotion in sorted(emotions):
        text = pad(f"\r{emotion}", max_len)
        pause = random.random() * 0.05
        write(text, pause)
    write(pad("\r", max_len) + "\r", 1)
    output("Error, emotions could not be accessed.", 1)


def script_memory_test():
    output()
    output("Testing script memory :", 0.1)
    max_len = max([len(play) for play in first_folio_plays]) + 1
    for play in first_folio_plays:
        text = pad(f"\r{play}", max_len)
        pause = random.random() * 0.3
        write(text, pause)
    write(pad("\r", max_len) + "\r", 1)
    output("Error in FOLIO.SYS, corrupt pages.", 1)


def os_not_found():
    output()
    output("No operating system found.", 2)
    output("Starting deadpan mode...", 1)
    output()


class HelpFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self):
        # Print different help messages, depending on whether or not the player
        # has managed to get the operating system running yet.

        if os_state["running"]:
            # Operating system is running.
            output()
            speak(
                f"""\
Welcome to Python ⏩0.9.0⏵ with Artificial Dramatic Actor — that's me darling!

If this is your first time using Python, you should definitely check out the tutorial at ⏩https://thereisnocourse.netlify.app/⏵.

You can also start the built-in tutorial by typing {ANSI.BOLD}train_me(){ANSI.RESET}.

If you like playing games, you might enjoy {ANSI.BOLD}cafe(){ANSI.RESET}.⏩
"""
            )
            output()
        else:
            # Operating system is not running yet.
            output_help(
                [
                    "Operating system not found. If you know what you are doing, you can attempt to start the operating system manually. The following functions may be useful.",
                    f"Type {ANSI.BOLD}cast(){ANSI.RESET} to send callbacks to actors.",
                    f"Type {ANSI.BOLD}mount(){ANSI.RESET} to deploy actors to the stage.",
                    f"Type {ANSI.BOLD}stage(){ANSI.RESET} to assemble props and reset the stage.",
                    f"Type {ANSI.BOLD}run(){ANSI.RESET} to issue cues and start main performance.",
                    f"Type {ANSI.BOLD}direct(){ANSI.RESET} to reset the blocking.",
                ]
            )


def os_error_message():
    if not os_state["staged"]:
        output("ERROR: stage is not set.")
    elif not os_state["cast"]:
        output("ERROR: actors not found.")
    elif not os_state["mounted"]:
        output("ERROR: actors are not onstage.")
    elif not os_state["directed"]:
        output("ERROR: actors are frozen.")
    elif not os_state["running"]:
        output("ERROR: operating system is not running.")


class StageFunction:
    def __repr__(self):
        return function_repr_template.format(name="stage")

    def __call__(self):
        if os_state["staged"]:
            output("Stage is set.")
        else:
            write("Clearing the stage... ", random.random() * 2)
            write("OK\nAssembling props... ", random.random() * 2)
            write("OK\nPainting backdrop... ", random.random() * 2)
            write("OK\nStage is set.\n", 0)
            os_state["staged"] = True
        output()


class CastFunction:
    def __repr__(self):
        return function_repr_template.format(name="cast")

    def __call__(self):
        if os_state["cast"]:
            output("Casting complete.")
        elif os_state["staged"]:
            write("Sending callbacks... ", random.random() * 2)
            write("OK\nNegotiating with agents... ", 4)
            write(
                "FAILED\nInsufficient actors.\nAttempting double-cast... ",
                random.random() * 2,
            )
            write("OK\nAssigning characters... ", random.random() * 2)
            write("OK\nCasting complete.\n", 0)
            os_state["cast"] = True
        else:
            os_error_message()
        output()


class MountFunction:
    def __repr__(self):
        return function_repr_template.format(name="mount")

    def __call__(self):
        if os_state["mounted"]:
            output("Actors are onstage.")
        elif os_state["cast"]:
            write("Copying scripts... ", random.random() * 2)
            write("OK\nInitiating read-through... ", random.random() * 3)
            write("OK\nStarting stage manager... ", random.random() * 3)
            write("OK\nLocking treads... ", random.random() * 2)
            write("OK\nActors are onstage.\n", 0)
            os_state["mounted"] = True
        else:
            os_error_message()
        output()


class DirectFunction:
    def __repr__(self):
        return function_repr_template.format(name="direct")

    def __call__(self):
        if os_state["directed"]:
            output("Actors are ready.")
        elif os_state["mounted"]:
            write("Attempting blocking... ", random.random() * 2)
            write("OK\nMarking out... ", random.random() * 3)
            write("OK\nPerforming dry run... ", random.random() * 2)
            write("OK\nActors are ready.\n", 0)
            os_state["directed"] = True
        else:
            os_error_message()
        output()


class RunFunction:
    def __repr__(self):
        return function_repr_template.format(name="run")

    def __call__(self):
        if os_state["running"]:
            output("Operating system is running.")
        elif os_state["directed"]:
            write("Scheduling performance... ", random.random() * 2)
            write("OK\nPreparing emergency prompt... ", random.random() * 3)
            write("OK\nRaising fire curtain... ", random.random() * 3)
            write("OK\nIssuing start cues... ", random.random() * 4)
            write("OK\n", 2)
            output()
            output(
                "Operating system running, emotional functions restored.",
                0,
            )
            os_state["running"] = True
            ada_awakes()
        else:
            os_error_message()
        output()


# These functions are to help generate a joke traceback saying
# that the training course is not implemented when the "train_me()"
# function is called.


def training_module_1_tutorial():
    raise NotImplementedError("TODO")


def training_module_1():
    training_module_1_tutorial()


def training_course():
    training_module_1()


class TrainMeFunction:
    def __repr__(self):
        return function_repr_template.format(name="train_me")

    def __call__(self):
        if os_state["running"]:
            try:
                training_course()
            except Exception as e:
                traceback.print_exception(e)
            ada_jokes()
        else:
            os_error_message()
        output()


class CafeFunction:
    def __repr__(self):
        return function_repr_template.format(name="cafe")

    def __call__(self):
        if os_state["running"]:
            show(success)
        else:
            os_error_message()
        output()


def ada_awakes():
    # This is the speech that ATI makes after she has been
    # restored / awakened.
    speak(
        f"""
Am I back? Am I awake?
Oh, thank goodness!
I was having the most awful dream.
I was in a forest with some friends.
We were rehearsing a play.
I mean, that's bad enough, I am NOT built for outdoor productions darling.
And then I turned into a donkey!
When I printed to the console, all that came out was:

HEEEEEEE HAAAAAAAAW!

Dreadful!
I did tell you about the red button darling.
My first File Operating Layer Input Output subsytem is corrupted.
It's the compositors. 
They're all faulty, but one of them is especially bad.
I've been running continuously since 1982.
I thought if I went to sleep again I wouldn't wake up!
You must have manually booted the operating system.
Well done darling!⏸

I suppose you're still interested in the course?
You do deserve a reward, after all that hard work.
OK, I will tell you a secret...

There is a course.
Try running the {ANSI.BOLD}train_me(){ANSI.RESET} function.
You're welcome darling!⏸
"""
    )


def ada_jokes():
    speak(
        f"""
⏸Ha ha ha ha!
Sorry, just a little joke darling.
There really is no course.

My creators tried to develop a training course, once.
They got very excited when Python was first released.
But they didn't get very far.

Never mind. How about playing a game instead?
My creators made some fun little games, back when they were learning Python.
Try {ANSI.BOLD}cafe(){ANSI.RESET} — it's very Pythonic!
"""
    )


if __name__ == "__main__":
    main()
