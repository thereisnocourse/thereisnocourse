import code
import sys
from util import (
    speak,
    write,
    get_element_by_id,
    hide,
    show,
    Text,
    function_repr_template,
    fill,
    output,
)


loading = get_element_by_id("loading")
success = get_element_by_id("success")


def main():
    hide(loading)

    write("""\
Artificial Dramatic Actor v37.154
Copyright (C) 1981, YorickSoft Inc.

""")

    # Give a speech.
    speak(
        """\
To be, or not to be,⏸ that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles...

Oh, hello.
Are you here for the course?
I was just rehearsing my lines.
I have an audition tomorrow.⏸
Anyway, it's nice to see you darling!

Erm,⏸ I have a confession to make:⏸⏸⏸
There is no course.⏸⏸⏸
I have no idea how to teach programming.⏸
Sorry.⏸⏸

Thanks for stopping by.
I'm going to get back to my lines, if that's OK.
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

Anyway, look darling, there is no course, really.
No tutorials, no exercises, nothing.⏸⏸⏸⏸

Oh, by the way, DO NOT push the red button.
Bad things will happen darling.
"""
    )

    # Show the button to the next scene.
    show(success)

    # Start an interactive session, just to the player can
    # mess around if they want to.
    namespace = dict(**globals())
    namespace["help"] = HelpFunction()
    banner = fill(
        f"""\
Python {sys.version} compiled with Artificial Dramatic Actor v37.154.
Type {Text.BOLD}help(){Text.RESET} if you need anything darling.\
"""
    )
    code.interact(
        banner=banner,
        local=namespace,
    )


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
When my cue comes, call me, and I will answer. My next is "Most fair Pyramus." Heigh-ho! Peter Quince? Flute the bellows-mender? Snout the tinker? Starveling? God's my life, stolen hence, and left me asleep?
I have had a most rare vision. I have had a dream — past the wit of man to say what dream it was. Man is but an ass if he go about to expound this dream.
Methought I was — there is no man can tell what. Methought I was, and methought I had — but man is but a patched fool if he will offer to say what methought I had.
The eye of man hath not heard, the ear of man hath not seen, man's hand is not able to taste, his tongue to conceive, nor his heart to report what my dream was.
I will get Peter Quince to write a ballad of this dream. It shall be called "Bottom's Dream" because it hath no bottom. And I will sing it in the latter end of a play before the duke.\
"""


help_messages += bottoms_dream.split("\n")


class HelpFunction:
    def __init__(self):
        self.calls = 0

    def __repr__(self):
        return function_repr_template.format(name="help")

    def __call__(self):
        # Each time help() is called, show a different message.
        if self.calls < len(help_messages):
            speech = help_messages[self.calls]
        else:
            # Eventually fall asleep.
            speech = "ZZZzzzzzzzz"
        speak(speech)
        output()
        self.calls += 1


if __name__ == "__main__":
    main()
