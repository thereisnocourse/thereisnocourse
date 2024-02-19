from pyscript import window, document, when
import js


session = dict(
    question="introduction",
)


def show(element, display="block"):
    element.style.display = display


def hide(element):
    element.style.display = "none"


@when("click", "#begin-button")
def on_click_begin(event):
    global session
    js.console.log("on_click_begin called")
    session["question"] = "0"
    window.history.pushState({}, "", "?question=0")
    render()


@when("submit", "#question0-form")
def on_question0_submit(event):
    global session
    js.console.log("on_question0_submit called")
    event.preventDefault()
    return False


def on_popstate(event):
    js.console.log("on_popstate called")
    js.console.log(event)
    render()


def render():
    query_params = dict(js.URLSearchParams.new(window.location.search))
    js.console.log(query_params)
    question = query_params.get("question", "introduction")
    js.console.log(question)
    session["question"] = question

    loading = document.querySelector("#loading")
    introduction = document.querySelector("#introduction")
    question0 = document.querySelector("#question0")
    question1 = document.querySelector("#question1")
    question2 = document.querySelector("#question2")
    question3 = document.querySelector("#question3")
    conclusion = document.querySelector("#conclusion")

    hide(loading)
    hide(introduction)
    hide(question0)
    hide(question1)
    hide(question2)
    hide(question3)
    hide(conclusion)

    question = session["question"]

    if question == "introduction":
        show(introduction)
        # TODO

    elif question == "0":
        show(question0)

    elif question == "1":
        show(question1)

    elif question == "2":
        show(question2)

    elif question == "3":
        show(question3)

    elif question == "conclusion":
        show(conclusion)

    else:
        # TODO don't hack my params
        pass


if __name__ == "__main__":
    window.addEventListener("popstate", on_popstate)
    render()
