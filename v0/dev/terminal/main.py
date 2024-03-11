from util import (
    get_element_by_id,
    hide,
    interact,
)


loading = get_element_by_id("loading")


def main():
    hide(loading)

    interact(
        banner="",
        local=globals(),
    )


if __name__ == "__main__":
    main()
