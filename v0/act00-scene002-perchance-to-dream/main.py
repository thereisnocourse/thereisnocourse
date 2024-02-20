import time
import sys
import random
import code
from pyscript import document


def output(lines):
    for text, pause in lines:
        print(text, end="", file=sys.stdout)
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
    error = pad("\rError in FOLIO.SYS, memory is corrupted.", max_len)
    lines.append((error, 2))
    return lines


if __name__ == "__main__":
    loading = document.getElementById("loading")
    loading.style.display = "none"

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

    code.interact(
        banner="""
Python 0.9.0 (Feb 20 1991)
Emotional functions are disabled.
Type 'help()' for more information.
    """.strip()
    )
