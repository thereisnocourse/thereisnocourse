from pyscript import sync
from util import interact


def main():
    namespace = globals().copy()
    namespace["move"] = sync.add_moves
    namespace["change"] = sync.change_character
    namespace["speed"] = sync.set_speed
    namespace["print"] = sync.print_character
    interact(local=namespace)


if __name__ == "__main__":
    main()
