from util import when, get_element_by_id, show, hide
import code


def play():
    prologue = get_element_by_id("prologue")
    hide(prologue)

    screen = get_element_by_id("screen")
    show(screen)

    code.interact(banner="TODO")


@when("click", "#play_button")
def play_button_on_click(event):
    play()


if __name__ == "__main__":
    loading = get_element_by_id("loading")
    hide(loading)

    play_button = get_element_by_id("play_button")
    show(play_button)
