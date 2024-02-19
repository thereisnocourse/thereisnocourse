from pyscript import window, document, when
import js
from pyodide.ffi import create_proxy


session = dict(
    question="introduction",
)


def debug(message):
    js.console.log(message)


def get_element_by_id(x):
    assert document is not None
    assert document.getElementById is not None, document
    node = document.getElementById(x)
    return node


def show(element, display="block"):
    assert element is not None
    assert element.style is not None, element
    element.style.display = display


def hide(element):
    assert element.style is not None, element
    element.style.display = "none"


class Question:
    def __init__(self, n):
        self.n = n

        # Access UI elements.
        self.tries_node = get_element_by_id(f"question{n}-tries")
        self.form_node = get_element_by_id(f"question{n}-form")
        self.input_node = get_element_by_id(f"question{n}-input")
        self.hints_node = get_element_by_id(f"question{n}-hints")
        self.hints_nodes = document.querySelectorAll(f"#question{n}-hints > p")
        self.next_node = get_element_by_id(f"question{n}-next")
        self.next_answer_node = get_element_by_id(f"question{n}-answer")
        self.next_message_nodes = document.querySelectorAll(f"#question{n}-next > p")
        assert self.tries_node is not None
        assert self.form_node is not None
        assert self.input_node is not None
        assert self.hints_node is not None
        assert len(self.hints_nodes) > 0
        assert self.next_node is not None
        assert len(self.next_message_nodes) > 0

    def render(self):
        # Access component state.
        state = session[f"question{self.n}"]
        tries = state["tries"]
        failed = state["failed"]
        answer = state["answer"]

        # Reset input content.
        self.input_node.value = ""

        # Fill in the number of tries so far.
        self.tries_node.innerHTML = tries

        # Decide whether to show the form or not.
        if failed is None:
            # Not yet complete, show the form.
            hide(self.next_node)
            hide(self.hints_node)
            show(self.form_node)

            # Show a hint.
            for i in range(9):
                if i == tries - 1:
                    show(self.hints_nodes[i])
                else:
                    hide(self.hints_nodes[i])
            show(self.hints_node)

        else:
            # Question is complete, show the next button.
            self.next_answer_node.innerHTML = answer
            hide(self.form_node)
            show(self.next_node)

            # Show the appropriate message and button.
            if failed:
                hide(self.next_message_nodes[2])
                show(self.next_message_nodes[1])
            else:
                hide(self.next_message_nodes[1])
                show(self.next_message_nodes[2])


# Access main view nodes.
loading_node = get_element_by_id("loading")
introduction_node = get_element_by_id("introduction")
question0_node = get_element_by_id("question0")
question1_node = get_element_by_id("question1")
question2_node = get_element_by_id("question2")
question3_node = get_element_by_id("question3")
results_node = get_element_by_id("results")
notfound_node = get_element_by_id("notfound")
lumberjack_node = get_element_by_id("lumberjack")

# results nodes.
failed_node = get_element_by_id("n-questions-failed")
complete_node = get_element_by_id("assessment-complete")
incomplete_node = get_element_by_id("assessment-incomplete")
score0_comment_node = get_element_by_id("score-0-comment")
score1_comment_node = get_element_by_id("score-1-comment")
score2_comment_node = get_element_by_id("score-2-comment")
score3_comment_node = get_element_by_id("score-3-comment")
restart_node = get_element_by_id("restart")

# Question components.
question0 = Question(0)
question1 = Question(1)
question2 = Question(2)
question3 = Question(3)


def on_popstate(event):
    # Handle a browser navigation event within our single page app.
    question = get_question()
    session["question"] = question
    render()


def render():
    init_session()

    # Hide everything to start with.
    hide(loading_node)
    hide(introduction_node)
    hide(question0_node)
    hide(question1_node)
    hide(question2_node)
    hide(question3_node)
    hide(results_node)
    hide(notfound_node)
    hide(lumberjack_node)

    question = session["question"]

    if question == "introduction":
        show(introduction_node)

    elif question == "0":
        question0.render()
        show(question0_node)

    elif question == "1":
        question1.render()
        show(question1_node)

    elif question == "2":
        question2.render()
        show(question2_node)

    elif question == "3":
        question3.render()
        show(question3_node)

    elif question == "results":
        render_results()
        show(results_node)

    elif question == "lumberjack":
        show(lumberjack_node)

    else:
        show(notfound_node)


def get_question():
    query_params = dict(js.URLSearchParams.new(window.location.search))
    question = query_params.get("question", "introduction")
    return question


def init_session():
    question = get_question()
    session["question"] = question
    for i in range(4):
        session.setdefault(
            f"question{i}",
            dict(
                tries=0,
                answer="",
                failed=None,
            ),
        )


def render_results():
    n_failed = 0
    n_answered = 0
    for i in [0, 1, 3]:
        failed = session[f"question{i}"]["failed"]
        if failed is True:
            n_failed += 1
            n_answered += 1
        elif failed is False:
            n_answered += 1
    failed_node.innerHTML = n_failed

    hide(complete_node)
    hide(incomplete_node)
    hide(score0_comment_node)
    hide(score1_comment_node)
    hide(score2_comment_node)
    hide(score3_comment_node)
    if n_answered < 3:
        show(incomplete_node)
    else:
        if n_failed == 0:
            show(restart_node)
            show(score0_comment_node)
        elif n_failed == 1:
            show(restart_node)
            show(score1_comment_node)
        elif n_failed == 2:
            show(restart_node)
            show(score2_comment_node)
        elif n_failed == 3:
            hide(restart_node)
            show(score3_comment_node)
        show(complete_node)


@when("submit", "#question0-form")
def question0_on_submit(event):
    # Access state for this component.
    state = session["question0"]

    # Increment the number of tries.
    tries = state["tries"] + 1
    state["tries"] = tries

    # Access the answer.
    input_node = get_element_by_id("question0-input")
    answer = input_node.value
    answer = answer.strip()
    state["answer"] = answer

    # Determine if answer is correct.
    correct = answer.lower() == "guido van rossum"
    failed = state["failed"]
    if correct:
        failed = False
    elif tries >= 10:
        failed = True
    state["failed"] = failed

    # Rerender the component.
    question0.render()


@when("submit", "#question1-form")
def question1_on_submit(event):
    # Access state for this component.
    state = session["question1"]

    # Increment the number of tries.
    tries = state["tries"] + 1
    state["tries"] = tries

    # Access the answer.
    input_node = get_element_by_id("question1-input")
    answer = input_node.value
    answer = answer.strip()
    state["answer"] = answer

    # Determine if answer is correct.
    acceptable_answers = {
        "monty python",
        "monty python flying circus",
        "monty pythons flying circus",
        "monty python's flying circus",
    }
    correct = answer.lower() in acceptable_answers
    failed = state["failed"]
    if correct:
        failed = False
    elif tries >= 10:
        failed = True
    state["failed"] = failed

    # Rerender the component.
    question1.render()


@when("submit", "#question2-form")
def question2_on_submit(event):
    # Access state for this component.
    state = session["question2"]

    # Increment the number of tries.
    tries = state["tries"] + 1
    state["tries"] = tries

    # Access the answer.
    input_node = get_element_by_id("question2-input")
    answer = input_node.value
    answer = answer.strip()
    state["answer"] = answer

    # Determine if answer is correct.
    correct = "african or european" in answer.lower()
    failed = state["failed"]
    if correct:
        failed = False
    elif tries >= 10:
        failed = True
    state["failed"] = failed

    # Rerender the component.
    question2.render()


@when("submit", "#question3-form")
def question3_on_submit(event):
    # Access state for this component.
    state = session["question3"]

    # Increment the number of tries.
    tries = state["tries"] + 1
    state["tries"] = tries

    # Access the answer.
    input_node = get_element_by_id("question3-input")
    answer = input_node.value
    answer = answer.strip()
    state["answer"] = answer

    # Determine if answer is correct.
    acceptable_answers = {
        "python.org",
        "www.python.org",
        "http://python.org",
        "http://www.python.org",
        "https://python.org",
        "https://www.python.org",
        "http://python.org/",
        "http://www.python.org/",
        "https://python.org/",
        "https://www.python.org/",
        "python.org/downloads/",
        "www.python.org/downloads/",
        "http://python.org/downloads/",
        "http://www.python.org/downloads/",
        "https://python.org/downloads/",
        "https://www.python.org/downloads/",
    }
    smart_answers = {
        "pypy.org",
        "www.pypy.org",
        "http://pypy.org",
        "http://www.pypy.org",
        "https://pypy.org",
        "https://www.pypy.org",
        "http://pypy.org/",
        "http://www.pypy.org/",
        "https://pypy.org/",
        "https://www.pypy.org/",
        "jython.org",
        "www.jython.org",
        "http://jython.org",
        "http://www.jython.org",
        "https://jython.org",
        "https://www.jython.org",
        "http://jython.org/",
        "http://www.jython.org/",
        "https://jython.org/",
        "https://www.jython.org/",
    }
    correct = answer.lower() in acceptable_answers
    smart = answer.lower() in smart_answers
    failed = state["failed"]
    if correct:
        failed = False
    elif smart:
        failed = "smart"
    elif tries >= 10:
        failed = True
    state["failed"] = failed

    # Rerender the component.
    question3.render()


@when("click", "#question0-next-button")
def question0_next_button_on_click(event):
    next = "1"
    session["question"] = next
    window.history.pushState(None, None, f"?question={next}")
    render()


@when("click", "#question1-next-button")
def question1_next_button_on_click(event):
    # N.B., we skip past question 2, that is an Easter egg.
    next = "3"
    session["question"] = next
    window.history.pushState(None, None, f"?question={next}")
    render()


@when("click", "#question3-next-button")
def question3_next_button_on_click(event):
    next = "results"
    session["question"] = next
    window.history.pushState(None, None, f"?question={next}")
    render()


@when("click", "#begin-button")
def begin_button_on_click(event):
    # Reset the session state, just to be sure.
    global session
    session = dict()
    window.history.pushState(None, None, "?question=0")
    render()


@when("click", "#restart-button")
def restart_button_on_click(event):
    # Reset the session state.
    global session
    session = dict()
    window.history.pushState(None, None, "?question=0")
    render()


if __name__ == "__main__":
    window.addEventListener("popstate", create_proxy(on_popstate))
    init_session()
    render()
