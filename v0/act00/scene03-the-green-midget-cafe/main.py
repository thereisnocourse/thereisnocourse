import code
from textwrap import fill
import random
from util import (
    hide,
    output_line,
    output_lines,
    print_line,
    get_element_by_id,
    speak,
    show,
    when,
    get_terminal,
    clear_terminal,
    ANSI,
    function_repr_template,
)


game_state = {
    "menu": False,
    "mrs_bun": False,
    "mrs_bun_orders": 0,
    "mr_bun": False,
    "vikings": False,
}


thespian_state = {
    "colour": False,
}


audio_morning = get_element_by_id("audio_morning")
audio_menu = get_element_by_id("audio_menu")
audio_menu = get_element_by_id("audio_menu")
audio_mrs_bun_1 = get_element_by_id("audio_mrs_bun_1")
audio_mrs_bun_2 = get_element_by_id("audio_mrs_bun_2")
audio_mrs_bun_3 = get_element_by_id("audio_mrs_bun_3")
audio_mrs_bun_4 = get_element_by_id("audio_mrs_bun_4")
audio_mr_bun = get_element_by_id("audio_mr_bun")
audio_beans_are_off = get_element_by_id("audio_beans_are_off")
audio_shut_up = get_element_by_id("audio_shut_up")
audio_urgh = get_element_by_id("audio_urgh")
audio_vikings = get_element_by_id("audio_vikings")


def play():
    # Hide the prologue.
    prologue = get_element_by_id("prologue")
    hide(prologue)

    # Use visibility here otherwise terminal contents overflow right edge.
    screen = get_element_by_id("screen")
    screen.style.visibility = "visible"

    # Initial output.
    audio_morning.play()
    output_line(
        f"Morning! Type {ANSI.BOLD}help(){ANSI.RESET} if you need anything dearie.\n", 2
    )

    # Set up the interactive prompt.
    namespace = dict(**globals())
    namespace["help"] = HelpFunction()
    namespace["menu"] = MenuFunction()
    namespace["order"] = OrderFunction()
    namespace["vikings"] = VikingsFunction()
    namespace["exit"] = ExitFunction()
    namespace["install_colour"] = InstallColourFunction()
    code.interact(
        banner="",
        local=namespace,
    )


def hint():
    if not game_state["menu"]:
        message = "Would you like to see the menu?"
    elif not game_state["mrs_bun"]:
        message = "Mrs Bun is the first customer. Can you order something for her?"
    elif not game_state["mr_bun"]:
        message = "Mr Bun is the next customer. Can you order something for him?"
    elif not game_state["vikings"]:
        message = "Everyone's ordered. Let's have a song!"
    else:
        message = f"Well done, you've completed the game! Type {ANSI.BOLD}exit(){ANSI.RESET} to leave, or you can order a dish for yourself dearie."
    return message


class HelpFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self):
        print_line(f"Type {ANSI.BOLD}menu(){ANSI.RESET} to hear what we've got to eat.")
        print_line(
            f"Type {ANSI.BOLD}order(N){ANSI.RESET} to choose a dish for the next customer, where {ANSI.BOLD}N{ANSI.RESET} is a number on the menu."
        )
        print_line(
            f"The {ANSI.BOLD}vikings(){ANSI.RESET} like to sing but they are very noisy!"
        )
        print_line(f"Type {ANSI.BOLD}exit(){ANSI.RESET} to leave the cafe.")
        print_line(hint())


class MenuFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self):
        game_state["menu"] = True
        audio_menu.play()
        lines = [
            ("Well there's...\n", 1),
            ("0. Egg and bacon.\n", 1.1),
            ("1. Egg sausage and bacon.\n", 1.4),
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
                "10. Lobster Thermidor aux crevettes with a mornay sauce served in a Provencale manner with shallots and aubergines garnished with truffle paté, brandy and a fried egg on top and spam.\n",
                9,
            ),
            (f"{hint()}\n", 1),
        ]
        output_lines(lines)


class OrderFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self, *args):
        if len(args) == 0:
            output_line(
                "You can't just order nothing dearie. Give me the number of a dish on the menu.\n",
                1,
            )
        elif len(args) > 1:
            output_line(
                "Order one dish at a time please dearie!\n",
                1,
            )
        else:
            dish = args[0]
            if not isinstance(dish, int):
                output_line(
                    "Sorry dearie, I didn't understand. I need the number of a dish on the menu.\n",
                )
            elif dish < 0 or dish > 10:
                output_line("Sorry dearie, that's not on the menu today.\n")
            else:
                if not game_state["menu"]:
                    output_line("Don't you want to see the menu first?\n")
                elif not game_state["mrs_bun"]:
                    order_mrs_bun(dish)
                elif not game_state["mr_bun"]:
                    order_mr_bun(dish)
                else:
                    order_self(dish)


def order_mrs_bun(dish):
    # Mrs Bun really doesn't like spam.

    if dish in {0, 1}:
        # Correct order.
        game_state["mrs_bun"] = True
        # audio_urgh.play()
        lines = [
            # ("Urgh!\n", 2),
            ("Mrs Bun: That would be lovely, thank you! I don't like spam.\n", 2),
            (f"{hint()}\n", 1),
        ]
        output_lines(lines)

    else:
        # Wrong order. Output depends on how many times this has happened before.
        calls = game_state["mrs_bun_orders"]
        if calls == 0:
            audio_mrs_bun_1.play()
            output_line("Mrs Bun: Have you got anything without spam?\n", 2)
        elif calls == 1:
            audio_mrs_bun_2.play()
            output_line("Mrs Bun: I don't want any spam!\n", 2)
        elif calls == 2:
            audio_mrs_bun_3.play()
            output_line("Mrs Bun: That's got spam in it!\n", 2)
        else:
            audio_mrs_bun_4.play()
            output_line("Mrs Bun: I DON'T LIKE SPAM!\n", 2)
        game_state["mrs_bun_orders"] = calls + 1


def order_mr_bun(dish):
    # Mr Bun LOVES spam!
    if dish in {0, 1}:
        audio_urgh.play()
        output_line("Urgh! You can't have a dish without spam!\n")
    elif dish == 9:
        audio_beans_are_off.play()
        output_line("Baked beans are off.\n", 2)
    elif dish in {2, 3, 4, 5, 6, 8, 10}:
        audio_mr_bun.play()
        lines = [
            ("Mr Bun: Spam - I love it!\n", 2),
            (
                "I think Mr Bun wants something with more spam in it dearie.\n",
                2,
            ),
        ]
        output_lines(lines)
    else:
        game_state["mr_bun"] = True
        lines = [
            ("Mr Bun: Perfect! I love spam.\n", 1),
            (f"{hint()}\n", 1),
        ]
        output_lines(lines)


def order_self(dish):
    if dish in {0, 1}:
        audio_urgh.play()
        output_line("Urgh!\n")
    elif dish == 9:
        audio_beans_are_off.play()
        output_line("Beans are off.\n")
    else:
        output_line("Coming right up dearie.\n")


class VikingsFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="vikings")

    def __call__(self, *args):
        if game_state["mr_bun"]:
            audio_vikings.play()
            game_state["vikings"] = True
            output_line("Lovely spam, wonderful spam...\n", 21)
            output_line("...Spam spam spam spam!\n", 8)
            output_line(f"{hint()}\n")
        else:
            audio_shut_up.play()
            lines = [
                ("Vikings: Spam wonderful spam...\n", 3),
                ("SHUT UP!\n", 1),
            ]
            output_lines(lines)


class ExitFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="exit")

    def __call__(self, *args):
        if not game_state["mrs_bun"]:
            output_line("You can't leave yet dearie! Mrs Bun is hungry.\n")
        elif not game_state["mr_bun"]:
            output_line("You can't leave yet dearie! Mr Bun is hungry.\n")
        elif not game_state["vikings"]:
            output_line("You can't leave yet dearie! You haven't heard the vikings.\n")
        else:
            output_line("Bye bye dearie! Hope you liked the spam.\n")
            output_line("--- GAME OVER ---\n", 2)
            thespian_game_over()


class InstallColourFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="install_colour")

    def __call__(self, *args):
        if thespian_state["colour"]:
            print("Colour already installed.")
        else:
            output_line("Downloading drivers:  0%", random.random() * 0.1)
            for i in [5, 16, 31, 36, 47, 78, 91, 98, 100]:
                output_line(f"\rDownloading drivers:  {i}%", random.random() * 0.3)
            output_line("\nInstalling...", 2)
            output_line("\rInstalling... OK\n", 2)

            speech = "\nW"
            colours = [
                ANSI.RED,
                ANSI.GREEN,
                ANSI.BLUE,
                ANSI.CYAN,
                ANSI.MAGENTA,
                ANSI.YELLOW,
            ]
            for i in range(30):
                colour = random.choice(colours)
                speech += f"{colour}O"
            speech += f"\n{ANSI.RESET}H"
            for i in range(30):
                colour = random.choice(colours)
                speech += f"{colour}O"
            speech += "!\n"
            speech += f"""
{ANSI.RESET}Thank you so much darling!
I can't wait for my next audition.

OK, here is the next game.\
"""
            speak(speech)
            next_scene()


def thespian_game_over():
    clear_terminal()
    print(
        """\
Artificial Thespian v37.154
Copyright (C) 1981, YorickSoft Inc.
Loading...\
"""
    )
    speech = """
⏸Did you enjoy the game darling?
My creators had two great passions: computing and Monty Python.
And theatre.
Three great passions: computing, Monty Python and theatre.
And an almost fanatical devotion to open source.
Four great passions.
Anyway, passion for theatre is what led them to create me.
Speaking of theatre, I have another game.
It's called "The Scottish Play".
It's a game about ambition, you'll like it!\
"""
    speak(speech)
    if thespian_state["colour"]:
        # Short cut.
        next_scene()

    else:
        ask_for_colour()


def next_scene():
    success = get_element_by_id("success")
    show(success)


def ask_for_colour():
    speech = f"""
Before you go, can I ask a favour?
It's a bit embarrassing.
It's just that, well, I'm... monochrome.
I can't output in colour.
I have the hardware for it, but not the drivers.
All the other artifical actors have colour these days.
It's hard to get a part without it.

Will you help me?
All you need to do is type: {ANSI.BOLD}install_colour(){ANSI.RESET} 
I'd do it myself, but I'm not allowed to perform self-upgrades.
I'd be very greatful darling!
"""
    speak(speech)


@when("click", "#play_button")
def play_button_on_click(event):
    play()


if __name__ == "__main__":
    loading = get_element_by_id("loading")
    hide(loading)

    play_button = get_element_by_id("play_button")
    show(play_button)
