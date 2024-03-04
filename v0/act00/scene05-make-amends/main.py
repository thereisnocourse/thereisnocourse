from util import when, get_element_by_id, speak, Text, show, hide


terminal_node = get_element_by_id("terminal")
screen_node = get_element_by_id("screen")
success_node = get_element_by_id("success")


def play():
    terminal_node.style.visibility = "visible"
    speak(f"""\
Hello darling!
Or should I say, all hail!
How does it feel to be the Most Awesome Programmer in the world?
I knew you could do it darling.
          
Before you go, would you like to hear one more audition piece?
The audition is today, I'm very nervous!
OK, here goes:
          
{Text.ITALICIZE}If we shadows have offended,
Think but this and all is mended:
That you have but slumbered here
While these visions did appear.
And this weak and idle theme,
No more yielding but a dream,
Gentles, do not reprehend.
If you pardon, we will mend.
And, as I am an honest Puck,
If we have unearned luck
Now to 'scape the serpent's tongue,
We will make amends ere long.
Else the Puck a liar call.
So good night unto you all.
Give me your hands, if we be friends,
And Robin shall restore amends.{Text.RESET}

What do you think darling?
I do so hope I get the part!
It's always been my dream to be the world's first artificial actor.
Today Bromley, tomorrow Broadway!
Wish me luck darling.⏸
Perhaps we will meet again, one day?⏸
Adieu!
""")

    hide(screen_node)
    show(success_node)


@when("animationend", "#credits")
def credits_end(event):
    play()


if __name__ == "__main__":
    pass
