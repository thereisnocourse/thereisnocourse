from pyscript import window, document, when
import js
from pyodide.ffi import create_proxy
from util import get_element_by_id, show, hide, get_url_params


# This variable stores the overall state of the UI in the current session (tab).
session = dict()


def init_session():
    # Initialise the session state.
    question = get_question_url_param()
    session["question"] = question
    for i in range(4):
        session.setdefault(
            f"question_{i}",
            dict(
                tries=0,
                answer="",
                failed=None,
            ),
        )


def get_question_url_param():
    params = get_url_params()
    question = params.get("question", "prologue")
    return question


class MainView:
    def __init__(self):
        # Access main UI elements.
        self.loading_node = get_element_by_id("loading")
        self.prologue_node = get_element_by_id("prologue")
        self.question_0_node = get_element_by_id("question_0")
        self.question_1_node = get_element_by_id("question_1")
        self.question_2_node = get_element_by_id("question_2")
        self.question_3_node = get_element_by_id("question_3")
        self.epilogue_node = get_element_by_id("epilogue")
        self.notfound_node = get_element_by_id("notfound")

    def render(self):
        # Ensure state is initialised.
        init_session()

        # Hide everything to start with.
        hide(self.loading_node)
        hide(self.prologue_node)
        hide(self.question_0_node)
        hide(self.question_1_node)
        hide(self.question_2_node)
        hide(self.question_3_node)
        hide(self.epilogue_node)
        hide(self.notfound_node)

        # Access state variable that determines which sub-view is visible.
        question = session["question"]

        # Render and show sub-view.
        if question == "prologue":
            show(self.prologue_node)

        elif question == "0":
            question_0_view.render()
            show(self.question_0_node)

        elif question == "1":
            question_1_view.render()
            show(self.question_1_node)

        elif question == "2":
            question_2_view.render()
            show(self.question_2_node)

        elif question == "3":
            question_3_view.render()
            show(self.question_3_node)

        elif question == "epilogue":
            epilogue_view.render()
            show(self.epilogue_node)

        else:
            show(self.notfound_node)


main_view = MainView()


class QuestionView:
    def __init__(self, n):
        self.n = n

        # Access UI elements.
        self.node = get_element_by_id(f"question_{n}")
        self.tries_node = get_element_by_id(f"question_{n}_tries")
        self.form_node = get_element_by_id(f"question_{n}_form")
        self.input_node = get_element_by_id(f"question_{n}_input")
        self.hints_node = get_element_by_id(f"question_{n}_hints")
        self.hints_nodes = document.querySelectorAll(f"#question_{n}_hints > p")
        self.next_node = get_element_by_id(f"question_{n}_next")
        self.next_answer_node = get_element_by_id(f"question_{n}_answer")
        self.next_message_nodes = document.querySelectorAll(f"#question_{n}_next > p")
        assert self.tries_node is not None
        assert self.form_node is not None
        assert self.input_node is not None
        assert self.hints_node is not None
        assert len(self.hints_nodes) > 0
        assert self.next_node is not None
        assert len(self.next_message_nodes) > 0

    def render(self):
        # Access component state.
        state = session[f"question_{self.n}"]
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


# Question views.
question_0_view = QuestionView(0)
question_1_view = QuestionView(1)
question_2_view = QuestionView(2)
question_3_view = QuestionView(3)


class EpilogueView:
    def __init__(self):
        # Access UI elements.
        self.failed_node = get_element_by_id("n_questions_failed")
        self.complete_node = get_element_by_id("assessment_complete")
        self.incomplete_node = get_element_by_id("assessment_incomplete")
        self.score_0_comment_node = get_element_by_id("score_0_comment")
        self.score_1_comment_node = get_element_by_id("score_1_comment")
        self.score_2_comment_node = get_element_by_id("score_2_comment")
        self.score_3_comment_node = get_element_by_id("score_3_comment")
        self.restart_node = get_element_by_id("restart")

    def render(self):
        n_failed = 0
        n_answered = 0
        for i in [0, 1, 3]:
            failed = session[f"question_{i}"]["failed"]
            if failed is True:
                n_failed += 1
                n_answered += 1
            elif failed is False:
                n_answered += 1
        self.failed_node.innerHTML = n_failed

        hide(self.complete_node)
        hide(self.incomplete_node)
        hide(self.score_0_comment_node)
        hide(self.score_1_comment_node)
        hide(self.score_2_comment_node)
        hide(self.score_3_comment_node)
        if n_answered < 3:
            show(self.incomplete_node)
        else:
            if n_failed == 0:
                show(self.restart_node)
                show(self.score_0_comment_node)
            elif n_failed == 1:
                show(self.restart_node)
                show(self.score_1_comment_node)
            elif n_failed == 2:
                show(self.restart_node)
                show(self.score_2_comment_node)
            elif n_failed == 3:
                hide(self.restart_node)
                show(self.score_3_comment_node)
            show(self.complete_node)


epilogue_view = EpilogueView()


def on_popstate(event):
    # Handle a browser navigation event within our single page app.
    question = get_question_url_param()
    session["question"] = question
    main_view.render()


@when("submit", "#question_0_form")
def question_0_on_submit(event):
    # Access state for this component.
    state = session["question_0"]

    # Increment the number of tries.
    tries = state["tries"] + 1
    state["tries"] = tries

    # Access the answer.
    input_node = get_element_by_id("question_0_input")
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
    question_0_view.render()


@when("submit", "#question_1_form")
def question_1_on_submit(event):
    # Access state for this component.
    state = session["question_1"]

    # Increment the number of tries.
    tries = state["tries"] + 1
    state["tries"] = tries

    # Access the answer.
    input_node = get_element_by_id("question_1_input")
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
    question_1_view.render()


@when("submit", "#question_2_form")
def question_2_on_submit(event):
    # Access state for this component.
    state = session["question_2"]

    # Increment the number of tries.
    tries = state["tries"] + 1
    state["tries"] = tries

    # Access the answer.
    input_node = get_element_by_id("question_2_input")
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
    question_2_view.render()


class SmartyPantsError(Exception):
    pass


@when("submit", "#question_3_form")
def question_3_on_submit(event):
    # Access state for this component.
    state = session["question_3"]

    # Increment the number of tries.
    tries = state["tries"] + 1
    state["tries"] = tries

    # Access the answer.
    input_node = get_element_by_id("question_3_input")
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

    # Update state.
    failed = state["failed"]
    if correct:
        failed = False
    elif smart:
        # Small joke here, try to catch people out trying to be smart :)
        raise SmartyPantsError()
    elif tries >= 10:
        failed = True
    state["failed"] = failed

    # Rerender the component.
    question_3_view.render()


@when("click", "#question_0_next_button")
def question_0_next_button_on_click(event):
    # Update session state.
    next = "1"
    session["question"] = next

    # Simulate navigation to a new page.
    window.history.pushState(None, None, f"?question={next}")
    main_view.render()


@when("click", "#question_1_next_button")
def question_1_next_button_on_click(event):
    # N.B., we skip past question 2, that is an Easter egg.

    # Update session state.
    next = "3"
    session["question"] = next

    # Simulate navigation to a new page.
    window.history.pushState(None, None, f"?question={next}")
    main_view.render()


@when("click", "#question_3_next_button")
def question_3_next_button_on_click(event):
    # Update session state.
    next = "epilogue"
    session["question"] = next

    # Simulate navigation to a new page.
    window.history.pushState(None, None, f"?question={next}")
    main_view.render()


@when("click", "#begin_button")
def begin_button_on_click(event):
    # Reset the session state, just to be sure.
    global session
    session = dict()

    # Simulate navigation to a new page.
    window.history.pushState(None, None, "?question=0")
    main_view.render()


@when("click", "#restart_button")
def restart_button_on_click(event):
    # Reset the session state.
    global session
    session = dict()

    # Simulate navigation to a new page.
    window.history.pushState(None, None, "?question=0")
    main_view.render()


if __name__ == "__main__":
    # Register a handler for back and forward navigation events.
    # https://jeff.glass/post/pyscript-why-create-proxy/
    window.addEventListener("popstate", create_proxy(on_popstate))

    # Render the main view.
    main_view.render()
