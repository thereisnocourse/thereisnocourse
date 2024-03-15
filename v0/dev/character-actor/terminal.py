from pyscript import sync, document
from util import (
    interact,
    speak,
    output,
    Text,
    get_element_by_id,
    get_terminal,
    get_terminal_cols,
    set_terminal_cols,
    fill,
    function_repr_template,
)


clue_node = get_element_by_id("clue")


class Help:
    """Type help() for your mission briefing."""

    def __repr__(self):
        return fill(function_repr_template.format(name="help")) + "\n"

    def __call__(self, *args):
        if len(args) == 0:
            self._tutorial()
        elif len(args) == 1:
            arg = args[0]
            output(arg.__doc__)
            output()

    def _tutorial(self):
        speak(
            """\
The compositor is made up of different rooms. Each room contains a 10x10 grid of cells. One of the cells in each room has been corrupted by a fruit emoji. You need to find the broken cell and fix it.
"""
        )

        clue_node.scrollIntoView(False)
        speak(
            f"""
Below the screen is a line from a script which has been corrupted. Use this as a {Text.BOLD}clue{Text.RESET} to figure out which character has been replaced by the fruit emoji.
"""
        )

        speak(
            f"""
To move around within the compositor, type {Text.BOLD}move(X){Text.RESET} where {Text.BOLD}X{Text.RESET} is a string of characters indicating the direction to move: "l" means left, "r" means right, "u" means up, "d" means down.

For example, to move one cell right:⏩
>>> ⏵⏸move("r")⏸
""",
        )
        sync.add_moves("r")

        speak("""
You can move more than one cell at a time. For example, to move two squares down and two squares left:⏩
>>> ⏵⏸move("ddll")⏸
""")
        sync.add_moves("ddll")

        speak(f"""
To save typing, you can use the {Text.BOLD}*{Text.RESET} operator to repeat moves. For example, to move right three times:⏩
>>> ⏵⏸move("r" * 3)⏸
""")
        sync.add_moves("r" * 3)

        speak("""
For example, to move left then up six times:⏩
>>> ⏵⏸move("lu" * 6)⏸
""")
        sync.add_moves("lu" * 6)

        speak(
            f"""
⏸To fix a broken cell in the compositor, type {Text.BOLD}print(X){Text.RESET} where {Text.BOLD}X{Text.RESET} is a string containing a single character.

For example, to print "a" in the current cell:⏩
>>> ⏵⏸print("a")⏸
"""
        )
        sync.print_character("a")

        speak(
            """
Your mission in each room is to find the fruit emoji, move to the broken cell, and print the correct character.
"""
        )

        speak(f"""
One more thing. Watch out for {Text.BOLD}agents{Text.RESET} which are moving characters that will try to capture you.

To evade the agents, type {Text.BOLD}change(){Text.RESET} to disguise yourself as a random character. For example:⏩
>>> ⏵⏸change()⏸
""")
        sync.change_character()

        speak(
            f"""
If you do get caught, type {Text.BOLD}escape(){Text.RESET} to get free again.
"""
        )

        speak("""
Good luck darling!
""")


def main():
    # Adjust terminal size for different font.
    # cols = get_terminal_cols()
    # set_terminal_cols(cols * 1.15)

    speak(f"""Type {Text.BOLD}help(){Text.RESET} for your mission briefing.""")
    output()

    namespace = globals().copy()
    namespace["move"] = sync.add_moves
    namespace["change"] = sync.change_character
    namespace["speed"] = sync.set_speed
    namespace["print"] = sync.print_character
    namespace["help"] = Help()
    interact(local=namespace)

    print("interaction ended")


if __name__ == "__main__":
    main()
