import code
from pyscript import sync


def main():
    namespace = globals().copy()
    namespace["move"] = sync.add_moves
    namespace["change"] = sync.change_character
    code.interact(banner="", local=namespace)


if __name__ == "__main__":
    main()
