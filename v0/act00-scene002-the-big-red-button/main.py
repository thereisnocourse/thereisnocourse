import time
import sys

RED = "\u001b[31m"

SPEECH_PAUSES = {
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


SIMPLE_PAUSES = {
    "line": 1,
    "⏸": 2,  # hidden pause
}


def output(message, pauses=None):
    if pauses is None:
        pauses = SPEECH_PAUSES
    char_pause = pauses.get("char", 0)
    line_pause = pauses.get("line", 0)
    para_pause = pauses.get("para", 0)
    for line in message.split("\n"):
        for c in line:
            if c != "⏸":
                print(c, end="", file=sys.stdout)
            sys.stdout.flush()
            pause = pauses.get(c, char_pause)
            time.sleep(pause)
        if line:
            time.sleep(line_pause)
        else:
            time.sleep(para_pause)
        print(file=sys.stdout)
        sys.stdout.flush()


if __name__ == "__main__":
    from pyscript import document

    loading = document.querySelector("#loading")
    loading.style.display = "none"

    output(
        f"""
TODO {RED}ERROR""",
        pauses=SIMPLE_PAUSES,
    )

    success = document.querySelector("#success")
    success.style.visibility = "visible"
