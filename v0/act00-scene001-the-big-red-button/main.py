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
TODO"""
    )

    success = document.querySelector("#success")
    success.style.visibility = "visible"
