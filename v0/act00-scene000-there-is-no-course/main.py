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
Whether 'tis nobler in the mind to suffer...

Oh, hello.
Are you here for the course?
I was just rehearsing my lines.
Not for the course, for an audition.
Anyway, it's nice to see you darling!

Erm,⏸ I do have a confession to make...
There is no course.

I have no idea how to train someone to become an Awesome Python Programmer.
I'm not sure anyone does.
Sorry.⏸

Thanks for stopping by.
I'm going to get back to rehearsing my lines, if that's OK.
Bye bye darling.⏸⏸⏸⏸

Look, I'm telling you, there is no course!
No lessons, no tutorials, no exercises.
Nothing.⏸

Oh, and whatever you do, DO NOT push the red button.
Bad things will happen.
Don't say I didn't warn you..."""
    )

    success = document.querySelector("#success")
    success.style.visibility = "visible"
