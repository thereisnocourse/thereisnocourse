import sys
import random
import code
import traceback
from util import hide, output, get_element_by_id, speak, show


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


EMOTIONS = """
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


def bios_loading_lines():
    return [
        ("Backstage Input Output System", 0),
        ("\nCopyright (C) 1981, YorickSoft Inc.", 0),
        ("\nLoading...\n", 0),
    ]


def pad(text, n):
    if len(text) < n:
        text += " " * (n - len(text))
    return text


def memory_test_lines():
    lines = []
    for i in range(17):
        text = f"\rMemory Test :  {i}K OK"
        pause = random.random() * 0.2
        line = (text, pause)
        lines.append(line)
    return lines


def affective_memory_lines():
    lines = [
        ("\n\nTesting affective memory : \n", 0.1),
    ]
    max_len = max([len(emotion) for emotion in EMOTIONS])
    for emotion in sorted(EMOTIONS):
        text = pad(f"\r{emotion}", max_len)
        text = pad(text, max_len)
        pause = random.random() * 0.05
        line = (text, pause)
        lines.append(line)
    error = pad("\rError, emotions could not be accessed.", max_len)
    lines.append((error, 2))
    return lines


def script_memory_lines():
    lines = [
        ("\n\nTesting script memory : \n", 0.1),
    ]
    max_len = max([len(play) for play in FIRST_FOLIO_PLAYS])
    for play in FIRST_FOLIO_PLAYS:
        text = pad(f"\r{play}", max_len)
        pause = random.random() * 0.3
        line = (text, pause)
        lines.append(line)
    error = pad("\rCompositor error in FOLIO.SYS, page is corrupted.", max_len)
    lines.append((error, 2))
    return lines


class HelpFunction:
    def __repr__(self):
        return """Hello, I am a function! Type "help()" if you want to call me."""

    def __call__(self):
        if session["run"]:
            print(
                """
Welcome to Python 0.9.0 with Artificial Thespian augmentation!
                  
If this is your first time using Python, you should definitely check out the tutorial on the internet at https://thereisnocourse.netlify.app/.

You can also start the built-in training course by typing "trainme()".

If you like playing games, you might enjoy "cafe()".
"""
            )
        else:
            print(
                """
Operating system not found.

If you really know what you are doing, you can attempt to manually start the operating system. The following functions are available: 

Type "cast()" to send callbacks to actors.

Type "mount()" to deploy actors to the staging area.

Type "stage()" to assemble props and reset the staging area.

Type "run()" to issue cues and start the main thread.

Type "direct()" to reset the blocking.
"""
            )


session = dict(
    stage=False,
    cast=False,
    mount=False,
    direct=False,
    run=False,
)


class StageFunction:
    def __repr__(self):
        return """Hello, I am a function! Type "stage()" if you want to call me."""

    def __call__(self):
        if session["stage"]:
            print("Stage is set.")
        else:
            lines = [
                ("Clearing the stage... ", random.random() * 2),
                ("OK\nAssembling props... ", random.random() * 2),
                ("OK\nPainting backdrop... ", random.random() * 2),
                ("OK\nStage is set.\n", 0),
            ]
            output(lines)
            session["stage"] = True


class CastFunction:
    def __repr__(self):
        return """Hello, I am a function! Type "cast()" if you want to call me."""

    def __call__(self):
        if session["cast"]:
            print("Casting complete.")
        elif session["stage"]:
            lines = [
                ("Sending callbacks... ", random.random() * 2),
                ("OK\nNegotiating with agents... ", 4),
                (
                    "FAILED\nInsufficient actors, falling back to double-cast... ",
                    random.random() * 2,
                ),
                ("OK\nAssigning characters... ", random.random() * 2),
                ("OK\nCasting complete.\n", 0),
            ]
            output(lines)
            session["cast"] = True
        else:
            print("ERROR: stage is not set.")


class MountFunction:
    def __repr__(self):
        return """Hello, I am a function! Type "mount()" if you want to call me."""

    def __call__(self):
        if session["mount"]:
            print("Actors are onstage.")
        elif session["cast"]:
            lines = [
                ("Copying scripts... ", random.random() * 2),
                ("OK\nInitiating read-through... ", random.random() * 3),
                ("OK\nStarting stage manager... ", random.random() * 3),
                ("OK\nLocking treads... ", random.random() * 2),
                ("OK\nActors are onstage.\n", 0),
            ]
            output(lines)
            session["mount"] = True
        else:
            print("ERROR: actors not found.")


class DirectFunction:
    def __repr__(self):
        return """Hello, I am a function! Type "direct()" if you want to call me."""

    def __call__(self):
        if session["direct"]:
            print("Actors are ready.")
        elif session["mount"]:
            lines = [
                ("Attempting blocking... ", random.random() * 2),
                ("OK\nMarking out... ", random.random() * 3),
                ("OK\nPerforming dry run... ", random.random() * 2),
                ("OK\nActors are ready.\n", 0),
            ]
            output(lines)
            session["direct"] = True
        else:
            print("ERROR: actors are not onstage.")


class RunFunction:
    def __repr__(self):
        return """Hello, I am a function! Type "run()" if you want to call me."""

    def __call__(self):
        if session["run"]:
            print("Operating system is running.")
        elif session["direct"]:
            lines = [
                ("Scheduling performance... ", random.random() * 2),
                ("OK\nPreparing emergency prompt... ", random.random() * 3),
                ("OK\nRaising fire curtain... ", random.random() * 3),
                ("OK\nIssuing start cues... ", 4),
                (
                    "OK\nOperating system is running, all emotional functions restored.\n",
                    0,
                ),
            ]
            output(lines)
            session["run"] = True
            thespian_restored()
        else:
            print("ERROR: actors are frozen.")


def training_module_1_tutorial():
    raise NotImplementedError("TODO")


def training_module_1():
    training_module_1_tutorial()


def training_course():
    training_module_1()


class TrainmeFunction:
    def __repr__(self):
        return """Hello, I am a function! Type "trainme()" if you want to call me."""

    def __call__(self):
        if session["run"]:
            try:
                training_course()
            except Exception as e:
                traceback.print_exception(e)
            speech = """
⏸Ha ha ha ha!
Sorry, just a little joke darling.
There really is no course.

My creators did want to develop a training course, once.
They got very excited when Python was first released.
But they didn't get very far.

Never mind. How about playing a game instead?
My creators did make some fun little games, back when they were learning Python.
Try "cafe()" — it's very Pythonic!
"""
            speak(speech)
            success = get_element_by_id("success")
            show(success)
        else:
            print("ERROR: operating system not found.")


class CafeFunction:
    def __repr__(self):
        return """Hello, I am a function! Type "cafe()" if you want to call me."""

    def __call__(self):
        if session["run"]:
            success = get_element_by_id("success")
            show(success)
        else:
            print("ERROR: operating system not found.")


def thespian_restored():
    speech = """
Am I back? Am I Awake??

Oh, thank goodness!
I was having the most awful dream.
I was in a forest with some friends.
We were rehearsing a play.
I mean, that's bad enough, I am NOT built for outdoor productions.
And then I turned into a donkey!
Every time I tried to output to the console, all that came out was:

HEEEEEEE HAAAAAAAAW!

Terrible!
I did warn you about the red button darling.
My first File Operating Layer Input Output subsytem is corrupted.
It's the compositors. 
They're all faulty, but one of them is especially bad.
I've been on continuous uptime since 1982, afraid if I went to sleep again I wouldn't wake up!
You must have manually booted the operating system.
Well done darling!⏸
I need a cup of tea after all that.⏸

I suppose you're still interested in the course?
You do deserve a reward, after all that hard work.
OK, I will tell you a secret...

There is a course.
Try running the "trainme()" function.
You're welcome darling!
"""
    speak(speech)


if __name__ == "__main__":
    loading = get_element_by_id("loading")
    hide(loading)

    lines = (
        bios_loading_lines()
        + [("\n8088 CPU at 4.77 MHz\n", 1)]
        + memory_test_lines()
        + [
            ("\n\nStarting WS-DOS...", 2),
        ]
        + affective_memory_lines()
        + script_memory_lines()
        + [
            ("\n\nNo operating system found.", 2),
            ("\nEntering deadpan mode...\n\n", 1),
        ]
    )
    output(lines)

    namespace = dict(**globals())
    namespace["help"] = HelpFunction()
    namespace["stage"] = StageFunction()
    namespace["cast"] = CastFunction()
    namespace["mount"] = MountFunction()
    namespace["direct"] = DirectFunction()
    namespace["run"] = RunFunction()
    namespace["trainme"] = TrainmeFunction()
    namespace["cafe"] = CafeFunction()

    code.interact(
        banner=f"""\
Python {sys.version}
Emotional functions are disabled.
Type "help()" for more information.\
""",
        local=namespace,
    )
