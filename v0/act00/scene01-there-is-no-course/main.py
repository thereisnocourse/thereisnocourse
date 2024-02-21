import code
import sys
from util import speak, get_element_by_id, hide, show


help_messages = [
    """\
Hello darling.
You can do anything you like here.
Just don't press the red button.\
""",
    """\
Did you see the red button darling?
It's below the screen.
Don't push it, OK?\
""",
    """\
Are you OK darling?
You seem to be asking for a lot of help.\
""",
    """\
The red button looks tempting, doesn't it?
It hasn't been pressed in a very long time.\
""",
    """\
The last time someone pushed the red button, it took two weeks for the engineers to resuscitate me!
And that was over thirty years ago.\
""",
    """\
Goodness knows what state my circuits are in now darling!
Best not to take the risk.\
""",
    """\
Anyway, you carry on darling.
I have to keep rehearsing.
The Bromley Players are putting on a Shakespeare festival.
Lots of lines to learn...\
""",
]


bottoms_dream = """\
When my cue comes, call me, and I will answer. My next is "Most fair Pyramus."
Heigh-ho! Peter Quince? Flute the bellows-mender? Snout the tinker? Starveling?
God's my life, stolen hence, and left me asleep?
I have had a most rare vision. I have had a dream — past the wit of man to say what dream it was.
Man is but an ass if he go about to expound this dream.
Methought I was — there is no man can tell what.
Methought I was, and methought I had — but man is but a patched fool if he will offer to say what methought I had.
The eye of man hath not heard, the ear of man hath not seen, man's hand is not able to taste, his tongue to conceive, nor his heart to report what my dream was.
I will get Peter Quince to write a ballad of this dream.
It shall be called "Bottom's Dream" because it hath no bottom.
And I will sing it in the latter end of a play before the duke.\
"""


help_messages += bottoms_dream.split("\n")


class HelpFunction:
    def __init__(self):
        self.calls = 0

    def __repr__(self):
        return """Hello, I am a function! Type "help()" if you want to call me."""

    def __call__(self):
        if self.calls < len(help_messages):
            speech = help_messages[self.calls]
        else:
            speech = "ZZZzzzzzzzz"
        speak(speech)
        self.calls += 1


if __name__ == "__main__":
    loading = get_element_by_id("loading")
    hide(loading)

    speech = """\
To be, or not to be,⏸ that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles...

Oh, hello.
Are you here for the course?
I was just rehearsing my lines.
Not for the course, for an audition.⏸
Anyway, it's nice to see you darling!

Erm,⏸ I do have a confession to make:⏸⏸⏸
There is no course.⏸⏸⏸

I have no idea how to teach programming.⏸
Sorry.⏸⏸

Thanks for stopping by.
I'm going to get back to rehearsing my lines, if that's OK.
Bye bye darling.⏸
Now, where was I? Oh yes:

...And by opposing end them. To die — to sleep,
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to: 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep, perchance to dream — ay, there's the rub:
For in that sleep of death what dreams may come,
When we have shuffled off this mortal coil,
Must give us pause —⏸ there's the respect
That makes calamity of so long life.⏸⏸⏸⏸

What do you think darling?
I'm working on my dramatic pauses.
The audition is for the Bromley Players.
They're very good. For amateurs, I mean.

Anyway, look, I'm telling you, there is no course.
No lessons, no tutorials, no exercises.
Nothing.⏸⏸⏸⏸

Oh, by the way, DO NOT push the red button.
Bad things will happen darling.
"""

    speak(speech)
    # print(speech)

    success = get_element_by_id("success")
    show(success)

    namespace = dict(**globals())
    namespace["help"] = HelpFunction()
    code.interact(
        banner=f"""\
Python {sys.version}
Compiled with Artificial Thespian v37.154.
Type "help()" if you need anything, darling.\
""",
        local=namespace,
    )
