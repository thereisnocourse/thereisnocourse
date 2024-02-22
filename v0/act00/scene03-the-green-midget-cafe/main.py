import sys
import random
import code
import traceback
from util import hide, output, get_element_by_id, speak, show


if __name__ == "__main__":
    loading = get_element_by_id("loading")
    hide(loading)

    lines = [
        ('Morning! Shout "help()" if you need anything dearie.\n', 1),
    ]
    output(lines)
    namespace = dict(**globals())
    code.interact(
        banner="",
        local=namespace,
    )
