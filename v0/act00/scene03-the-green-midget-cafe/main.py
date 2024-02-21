import sys
import random
import code
import traceback
from util import hide, output, get_element_by_id, speak, show


if __name__ == "__main__":
    loading = get_element_by_id("loading")
    hide(loading)

    print("TODO")

    namespace = dict(**globals())
    code.interact(
        banner=f"""\
The Green Midget Cafe
Type "help()" for more information.\
""",
        local=namespace,
    )
