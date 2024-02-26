from util import when, get_element_by_id, show, hide
import code


game_state = {
    "location": "outside",
    "objects_held": set(),
    "hall_lit": False,
    "prophecy_heard": False,
    "computer_destroyed": False,
    "forest_defeated": False,
}


class InteractionComplete(SystemExit):
    pass


def play():
    prologue = get_element_by_id("prologue")
    hide(prologue)

    screen = get_element_by_id("screen")
    show(screen)

    while not game_state["forest_defeated"]:
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
    loading = get_element_by_id("loading")
    hide(loading)

    play_button = get_element_by_id("play_button")
    show(play_button)
