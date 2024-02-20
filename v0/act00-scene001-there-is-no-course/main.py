import time
import sys


speech_pauses = {
    "para": 2,  # pause between paragraphs
    "char": 0.07,  # default pause between characters
    ",": 0.5,
    ";": 0.5,
    ":": 0.5,
    "—": 0.5,
    ".": 1,
    "!": 1,
    "?": 1,
    "⏸": 2,  # hidden pause
}


def speak(message):
    char_pause = speech_pauses["char"]
    para_pause = speech_pauses["para"]
    for line in message.split("\n"):
        for c in line:
            if c != "⏸":
                print(c, end="", file=sys.stdout)
            sys.stdout.flush()
            pause = speech_pauses.get(c, char_pause)
            time.sleep(pause)
        if not line:
            time.sleep(para_pause)
        print(file=sys.stdout)
        sys.stdout.flush()


if __name__ == "__main__":
    from pyscript import document

    loading = document.querySelector("#loading")
    loading.style.display = "none"

    speak(
        """\
To be, or not to be,⏸ that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles...

Oh, hello.
Are you here for the course?
I was just rehearsing my lines.
Not for the course, for an audition.⏸⏸
Anyway, it's nice to see you darling!

Erm,⏸ I do have a confession to make:⏸⏸⏸⏸
There is no course.⏸⏸⏸⏸

I have no idea how to teach programming.⏸
I'm not sure anyone does.⏸
Sorry.⏸⏸

Thanks for stopping by.
I'm going to get back to rehearsing my lines, if that's OK.
Bye bye darling.⏸⏸
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
That makes calamity of so long life.⏸⏸⏸⏸⏸

What do you think darling? 
I'm working on my dramatic pauses.
The audition is for the Bromley Players.
They're very good. For amateurs, I mean.

Anyway, look, I'm telling you, there is no course.
No lessons, no tutorials, no exercises.
Nothing.⏸⏸⏸⏸

Oh, by the way, DO NOT push the red button.
Bad things will happen.
Don't say I didn't warn you darling.
"""
    )

    success = document.getElementById("success")
    success.style.visibility = "visible"
