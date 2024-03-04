import code
import random
from util import (
    hide,
    output_help,
    write,
    output,
    get_element_by_id,
    speak,
    show,
    when,
    clear_terminal,
    Text,
    ANSI,
    function_repr_template,
)


# Initialise the game state.
game_state = {
    "menu": False,
    "mrs_bun": False,
    "mrs_bun_orders": 0,
    "mr_bun": False,
    "vikings": False,
}


# Initialise the state of ADA.
ada_state = {
    "colour": False,
}


# Access the DOM nodes we need.
loading_node = get_element_by_id("loading")
play_button_node = get_element_by_id("play_button")
audio_morning_node = get_element_by_id("audio_morning")
audio_menu_node = get_element_by_id("audio_menu")
audio_mrs_bun_1_node = get_element_by_id("audio_mrs_bun_1")
audio_mrs_bun_2_node = get_element_by_id("audio_mrs_bun_2")
audio_mrs_bun_3_node = get_element_by_id("audio_mrs_bun_3")
audio_mrs_bun_4_node = get_element_by_id("audio_mrs_bun_4")
audio_mr_bun_node = get_element_by_id("audio_mr_bun")
audio_beans_are_off_node = get_element_by_id("audio_beans_are_off")
audio_shut_up_node = get_element_by_id("audio_shut_up")
audio_urgh_node = get_element_by_id("audio_urgh")
audio_vikings_node = get_element_by_id("audio_vikings")
prologue_node = get_element_by_id("prologue")
screen_node = get_element_by_id("screen")
success_node = get_element_by_id("success")


def play():
    # Hide the prologue.
    hide(prologue_node)

    # Use visibility here otherwise terminal contents overflow right edge.
    screen_node.style.visibility = "visible"

    # Initial output.
    audio_morning_node.play()
    output("Morning!", 1)
    output(f"Type {Text.BOLD}help(){Text.RESET} if you need anything dearie.", 1)

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
        message = f"Well done, you've completed the game! Type {Text.BOLD}exit(){Text.RESET} to leave, or you can order a dish for yourself dearie."
    return message


class HelpFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self):
        output_help(
            [
                f"Type {Text.BOLD}menu(){Text.RESET} to hear what we've got to eat.",
                f"Type {Text.BOLD}order(N){Text.RESET} to choose a dish for the next customer, where {Text.BOLD}N{Text.RESET} is a number on the menu.",
                f"The {Text.BOLD}vikings(){Text.RESET} like to sing but they are very noisy!",
                f"Type {Text.BOLD}exit(){Text.RESET} to leave the cafe.",
                hint(),
            ]
        )


class MenuFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self):
        game_state["menu"] = True
        audio_menu_node.play()
        lines = [
            ("Well there's...", 1),
            ("0. Egg and bacon.", 1.1),
            ("1. Egg sausage and bacon.", 1.4),
            ("2. Egg and spam.", 0.9),
            ("3. Egg bacon and spam.", 1.9),  # 6.0
            ("4. Egg bacon sausage and spam.", 2),  # 8.0
            ("5. Spam bacon sausage and spam.", 2.1),  # 10.1
            ("6. Spam egg spam spam bacon and spam.", 3.1),  # 13.2
            (
                "7. Spam sausage spam spam spam bacon spam tomato and spam.",
                4.9,
            ),  # 18.1
            ("8. Spam spam spam egg and spam.", 3),  # 21.1
            (
                "9. Spam spam spam spam spam spam baked beans spam spam spam and spam.",
                7.9,  # 29.0
            ),
            ("Or...", 0),
            (
                "10. Lobster Thermidor aux crevettes with a mornay sauce served in a Provencale manner with shallots and aubergines garnished with truffle paté, brandy and a fried egg on top and spam.",
                9,
            ),
            ("", 0),
            (hint(), 1),
        ]
        for text, pause in lines:
            output(text, pause)


class OrderFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="help")

    def __call__(self, *args):
        if len(args) == 0:
            output(
                "You can't just order nothing dearie. Give me the number of a dish on the menu.",
                1,
            )
        elif len(args) > 1:
            output(
                "Order one dish at a time please dearie!",
                1,
            )
        else:
            dish = args[0]
            if not isinstance(dish, int):
                output(
                    "Sorry dearie, I didn't understand. I need the number of a dish on the menu.",
                )
            elif dish < 0 or dish > 10:
                output("Sorry dearie, that's not on the menu today.")
            else:
                if not game_state["menu"]:
                    output("Don't you want to see the menu first?")
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
        output("Mrs Bun: That would be lovely, thank you! I don't like spam.", 2)
        output()
        output(hint(), 1)

    else:
        # Wrong order. Output depends on how many times this has happened before.
        calls = game_state["mrs_bun_orders"]
        if calls == 0:
            audio_mrs_bun_1_node.play()
            output("Mrs Bun: Have you got anything without spam?", 2)
        elif calls == 1:
            audio_mrs_bun_2_node.play()
            output("Mrs Bun: I don't want any spam!", 2)
        elif calls == 2:
            audio_mrs_bun_3_node.play()
            output("Mrs Bun: That's got spam in it!", 2)
        else:
            audio_mrs_bun_4_node.play()
            output("Mrs Bun: I DON'T LIKE SPAM!", 2)
        game_state["mrs_bun_orders"] = calls + 1


def order_mr_bun(dish):
    # Mr Bun LOVES spam!
    if dish in {0, 1}:
        audio_urgh_node.play()
        output("Urgh! You can't have a dish without spam!")
    elif dish == 9:
        audio_beans_are_off_node.play()
        output("Baked beans are off.", 2)
    elif dish in {2, 3, 4, 5, 6, 8, 10}:
        audio_mr_bun_node.play()
        output("Mr Bun: Spam - I love it!", 2)
        output()
        output(
            "I think Mr Bun wants something with more spam in it dearie.",
            2,
        )
    else:
        game_state["mr_bun"] = True
        output("Mr Bun: Perfect! I love spam.", 1)
        output()
        output(hint(), 1)


def order_self(dish):
    if dish in {0, 1}:
        audio_urgh_node.play()
        output("Urgh!")
    elif dish == 9:
        audio_beans_are_off_node.play()
        output("Beans are off.")
    else:
        output("Coming right up dearie.")


class VikingsFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="vikings")

    def __call__(self, *args):
        if game_state["mr_bun"]:
            audio_vikings_node.play()
            game_state["vikings"] = True
            output("Lovely spam, wonderful spam...", 21)
            output("...Spam spam spam spam!", 8)
            output()
            output(hint())
        else:
            audio_shut_up_node.play()
            output("Vikings: Spam wonderful spam...", 3)
            output("SHUT UP!", 1)


class ExitFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="exit")

    def __call__(self, *args):
        if not game_state["mrs_bun"]:
            output("You can't leave yet dearie! Mrs Bun is hungry.")
        elif not game_state["mr_bun"]:
            output("You can't leave yet dearie! Mr Bun is hungry.")
        elif not game_state["vikings"]:
            output("You can't leave yet dearie! You haven't heard the vikings.")
        else:
            output("Bye bye dearie! Hope you liked the spam.", 2)
            output("--- GAME OVER ---", 2)
            game_over()


class InstallColourFunction:
    def __repr__(self):
        # Customise repr to assist players who forget to add "()" to call a function.
        return function_repr_template.format(name="install_colour")

    def __call__(self, *args):
        if ada_state["colour"]:
            output("Colour drivers already installed.")
        else:
            write("Downloading drivers:  0%", random.random() * 0.1)
            for i in [5, 16, 31, 36, 47, 78, 91, 98, 100]:
                write(f"\rDownloading drivers:  {i}%", random.random() * 0.3)
            write("\nInstalling...", 2)
            write("\rInstalling... OK\n", 2)

            colours = [
                ANSI.RED,
                ANSI.GREEN,
                ANSI.BLUE,
                ANSI.CYAN,
                ANSI.MAGENTA,
                ANSI.YELLOW,
                ANSI.BRIGHT_RED,
                ANSI.BRIGHT_GREEN,
                ANSI.BRIGHT_BLUE,
                ANSI.BRIGHT_CYAN,
                ANSI.BRIGHT_MAGENTA,
                ANSI.BRIGHT_YELLOW,
            ]
            bg_colours = [
                ANSI.BG_RED,
                ANSI.BG_GREEN,
                ANSI.BG_BLUE,
                ANSI.BG_CYAN,
                ANSI.BG_MAGENTA,
                ANSI.BG_YELLOW,
                ANSI.BG_BRIGHT_RED,
                ANSI.BG_BRIGHT_GREEN,
                ANSI.BG_BRIGHT_BLUE,
                ANSI.BG_BRIGHT_CYAN,
                ANSI.BG_BRIGHT_MAGENTA,
                ANSI.BG_BRIGHT_YELLOW,
            ]
            write("\nW", 0.03)
            for i in range(30):
                colour = random.choice(colours)
                bg_colour = random.choice(bg_colours)
                write(f"{bg_colour}{colour}O", 0.03)
            write(f"\n{ANSI.RESET}H", 0.03)
            for i in range(30):
                colour = random.choice(colours)
                bg_colour = random.choice(bg_colours)
                write(f"{bg_colour}{colour}O", 0.03)
            write(f"!\n{ANSI.RESET}", 2)
            speech = """
Thank you so much darling!
I can't wait for my next audition.

Well darling, would you like to play another game?
I have a good one, it's all about ambition and power.
You're going to love it!
"""
            speak(speech)
            next_scene()


def game_over():
    clear_terminal()
    print(
        """\
Artificial Dramatic Actor v37.154
Copyright (C) 1981, YorickSoft Inc.
"""
    )
    speech = """
⏸Did you enjoy the game darling?
My creators had two chief passions: computing and Monty Python.
And theatre.
Three chief passions: computing, Monty Python and theatre.
And an almost fanatical devotion to open source.
Four chief passions.
Anyway, passion for theatre is what led them to create me.
"""
    speak(speech)
    if ada_state["colour"]:
        # Short cut.
        next_scene()

    else:
        ask_for_colour()


def next_scene():
    show(success_node)


def ask_for_colour():
    speech = f"""
Darling, could I ask a favour?
It's a bit embarrassing.
It's just that, well, I'm... monochrome.
I can't output in colour.
I have the hardware for it, but not the drivers.
All the other artifical actors have colour these days.
It's hard to get a good part without it.

Will you help me?
All you need to do is type: {Text.BOLD}install_colour(){Text.RESET} 
I'd do it myself, but I'm not allowed to perform self-upgrades.
I'd be very grateful darling!
"""
    speak(speech)


@when("click", "#play_button")
def play_button_on_click(event):
    play()


if __name__ == "__main__":
    hide(loading_node)
    show(play_button_node)
