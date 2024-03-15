from util import (
    get_element_by_id,
    hide,
    interact,
)


loading = get_element_by_id("loading")


def main():
    hide(loading)

    try:
        interact(
            banner="",
            local=globals(),
        )
    except SystemExit:
        pass

    print("interaction ended")


if __name__ == "__main__":
    main()
