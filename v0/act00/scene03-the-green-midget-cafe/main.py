import sys
import random
import code
import traceback
from util import hide, output, get_element_by_id, speak, show, when, query_selector_all


game_state = {
    "menu": False,
    "mrs_bun": False,
    "mr_bun": False,
    "vikings": False,
}


def play():
    prologue = get_element_by_id("prologue")
    hide(prologue)
    screen = get_element_by_id("screen")
    show(screen)
    audio = get_element_by_id("audio")
    show(audio)

    audio_morning = get_element_by_id("audio_morning")
    show(audio_morning)
    audio_morning.play()

    lines = [
        ('Morning! Shout "help()" if you need anything dearie.\n', 1),
    ]
    output(lines)

    namespace = dict(**globals())
    namespace["help"] = HelpFunction()
    namespace["menu"] = MenuFunction()
    code.interact(
        banner="",
        local=namespace,
    )


function_repr_template = (
    'Hello, I am a function! Type "{name}()" if you want me to do something.'
)


class HelpFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self):
        print(
            """
Hello dearie! Type "menu()" to hear what we've got to eat.
              
Type "order(N)" to choose a dish for the next customer, where N is a number on the menu.

Don't encourage the "vikings()" they are very noisy singers!
"""
        )


class MenuFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self):
        for element in query_selector_all("#audio>audio"):
            hide(element)
        audio_menu = get_element_by_id("audio_menu")
        show(audio_menu)
        audio_menu.play()
        menu_items = [
            ("\nWell there's...\n", 1),
            ("0. Egg and bacon.\n", 1),
            ("1. Egg sausage and bacon.\n", 1.2),
            ("2. Egg and spam.\n", 0.9),
            ("3. Egg bacon and spam.\n", 1.9),  # 6.0
            ("4. Egg bacon sausage and spam.\n", 2),  # 8.0
            ("5. Spam bacon sausage and spam.\n", 2.1),  # 10.1
            ("6. Spam egg spam spam bacon and spam.\n", 3.1),  # 13.2
            (
                "7. Spam sausage spam spam spam bacon spam tomato and spam.\n",
                4.9,
            ),  # 18.1
            ("8. Spam spam spam egg and spam.\n", 3),  # 21.1
            (
                "9. Spam spam spam spam spam spam baked beans spam spam spam and spam.\n",
                7.9,  # 29.0
            ),
            (
                "10. Lobster Thermidor aux crevettes with a mornay sauce served in a Provencale manner with shallots and aubergines garnished with truffle paté, brandy and a fried egg on top and spam.\n\n",
                9,
            ),
        ]
        output(menu_items)


@when("click", "#play_button")
def play_button_on_click(event):
    play()


if __name__ == "__main__":
    loading = get_element_by_id("loading")
    hide(loading)

    play_button = get_element_by_id("play_button")
    show(play_button)
