import time
import sys


if __name__ == "__main__":
    from pyscript import document

    loading = document.querySelector("#section-loading")
    loading.style.display = "none"

    intro = document.querySelector("#section-introduction")
    intro.style.display = "block"
