from util import when, get_element_by_id, show, hide, output, get_terminal
import code


game_state = {
    "location": "outside",
    "possessions": set(),
    "hall_lit": False,
    "prophecy_heard": False,
    "computer_destroyed": False,
    "forest_destroyed": False,
    "game_over": False,
}


class InteractionComplete(SystemExit):
    pass


loading_node = get_element_by_id("loading")
play_button_node = get_element_by_id("play_button")
prologue_node = get_element_by_id("prologue")
screen_node = get_element_by_id("screen")
terminal = get_terminal()


def play():
    hide(prologue_node)
    show(screen_node)

    try:
        code.interact(local=globals())
    except InteractionComplete:
        output("Interaction complete.")

    while not game_state["game_over"]:
        location = game_state["location"]
        if location == "outside":
            play_outside()
        elif location == "hall":
            play_hall()
        elif location == "dungeon":
            play_dungeon()
        elif location == "bedroom":
            play_bedroom()
        elif location == "battlements":
            play_battlements()
        else:
            raise RuntimeError("unexpected location")

    game_completed()


def play_outside():
    pass


def play_hall():
    pass


def play_dungeon():
    pass


def play_bedroom():
    pass


def play_battlements():
    pass


def game_completed():
    pass


@when("click", "#play_button")
def play_button_on_click(event):
    play()


if __name__ == "__main__":
    hide(loading_node)
    show(play_button_node)
