from collections import deque, Counter
import random
import csv
from util import (
    get_element_by_id,
    hide,
    show,
    html_speak,
)
from pyscript import document
import js
from pyodide.ffi import create_proxy
import asyncio
import emoji


screen_node = get_element_by_id("screen")
terminal_node = get_element_by_id("terminal")
canvas_container_node = get_element_by_id("canvas_container")
loading_node = get_element_by_id("loading")
outro_node = get_element_by_id("outro")
success_node = get_element_by_id("success")
clue_node = get_element_by_id("clue")
clue_container_node = get_element_by_id("clue_container")
info_node = get_element_by_id("info")
moves_node = get_element_by_id("moves")
position_node = get_element_by_id("position")
speed_node = get_element_by_id("speed")
speed = 3
rows_per_room = 10
cols_per_room = 10
default_player_character = "🕵️"
disguises = emoji.smileys + emoji.people + emoji.nature
transformations = (
    (1, 1, "a"),
    (7, 18, "u"),
    (5, 24, "n"),
    (18, 21, "i"),
    (15, 14, "c"),
    (11, 8, "o"),
    (24, 5, "d"),
    (22, 18, "e"),
)
blocks = emoji.blocks + ["🔒"]


def speed_command(new_speed):
    global speed
    speed = new_speed


def move_command(moves):
    player.add_moves(moves)


def check_char(c):
    if not isinstance(c, str):
        raise TypeError("must be a string")
    if len(c) != 1:
        raise ValueError("must be a string of length 1")


def change_command(*args):
    if len(args) == 0:
        player.change()
    elif len(args) == 1:
        character = args[0]
        check_char(character)
        player.change(character)


def print_command(character):
    check_char(character)
    player.print(character)

    # Check to see if all replacements have been solved.
    solved = True
    for row, col, character in transformations:
        printed = world[row][col]
        solved = solved and (character == printed)
    if solved:
        world[28][29] = ""


def escape_command():
    player.captured = False


def col_to_text_x(col):
    return ((col % cols_per_room) * cell_width) + (cell_width / 2)


def row_to_text_y(row):
    return ((row % rows_per_room) * cell_width) + (cell_width / 2) + 3


SEARCHING = 0
CHASING = 1


class Agent:
    def __init__(self, row, col, character, recognition):
        self.row = row
        self.col = col
        self.character = character
        self.recognition = recognition
        self.observations = Counter()
        self.state = SEARCHING

    def move(self):
        # Make an observation, update state.
        self.state = SEARCHING
        if self.room == player.room and not player.captured:
            self.observations[player.character] += 1
            if self.observations[player.character] > self.recognition:
                self.state = CHASING

        # N.B., row coords are counted from the top.
        move = None

        # Discover what moves are possible.
        possible = ""
        if self.row > 0:
            up_char = world[self.row - 1][self.col]
            if up_char not in blocks:
                possible += "u"
        if self.row < len(world) - 1:
            down_char = world[self.row + 1][self.col]
            if down_char not in blocks:
                possible += "d"
        if self.col > 0:
            left_char = world[self.row][self.col - 1]
            if left_char not in blocks:
                possible += "l"
        if self.col < len(world[self.row]) - 1:
            right_char = world[self.row][self.col + 1]
            if right_char not in blocks:
                possible += "r"

        if self.state == SEARCHING:
            # Move in a random direction.
            move = random.choice(possible)

        elif self.state == CHASING:
            # Move towards the player.
            if player.row < self.row and "u" in possible:
                move = "u"
            elif player.row > self.row and "d" in possible:
                move = "d"
            elif player.col < self.col and "l" in possible:
                move = "l"
            elif player.col > self.col and "r" in possible:
                move = "r"

        # Make the move.
        if move == "d":
            self.row = self.row + 1
        elif move == "u":
            self.row = self.row - 1
        elif move == "r":
            self.col = self.col + 1
        elif move == "l":
            self.col = self.col - 1

        # Make the capture.
        if self.state == CHASING and self.row == player.row and self.col == player.col:
            player.captured = True
            # Clear out any pending moves.
            player.moves.clear()

    @property
    def text_x(self):
        return col_to_text_x(self.col)

    @property
    def text_y(self):
        return row_to_text_y(self.row)

    @property
    def room(self):
        return (self.row // rows_per_room, self.col // cols_per_room)

    def render(self):
        if self.room == player.room:
            if self.state == CHASING:
                x = (self.col % cols_per_room) * cell_width
                y = (self.row % rows_per_room) * cell_height
                ctx.fillStyle = "red"
                ctx.fillRect(
                    x,
                    y,
                    cell_width,
                    cell_height,
                )
            ctx.fillStyle = "black"
            ctx.fillText(self.character, self.text_x, self.text_y)


class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.character = default_player_character
        self.moves = deque()
        self.printed = None
        self.captured = False
        self.disguises_used = {self.character}

    def add_moves(self, moves):
        self.moves.extend(list(moves.lower()))

    def move(self):
        if self.captured:
            return
        try:
            move = self.moves.popleft()
        except IndexError:
            pass
        else:
            # N.B., row coords are counted from the top.
            if move == "d":
                new_row = self.row + 1
                new_col = self.col
            elif move == "u":
                new_row = self.row - 1
                new_col = self.col
            elif move == "r":
                new_row = self.row
                new_col = self.col + 1
            elif move == "l":
                new_row = self.row
                new_col = self.col - 1

            # # Out of bounds checks.
            # if new_row < 0:
            #     return
            # if new_row > rows - 1:
            #     return
            # if new_col < 0:
            #     return
            # if new_col > cols - 1:
            #     return

            # Stop checks.
            new_char = world[new_row][new_col]
            if new_char in blocks:
                return

            self.row = new_row
            self.col = new_col

    def change(self, character=None):
        if character is None:
            character = random.choice(disguises)
            while character in self.disguises_used:
                character = random.choice(disguises)
        else:
            check_char(character)
        self.character = character
        self.disguises_used.add(character)

    def print(self, character):
        if not self.captured:
            world[self.row][self.col] = character
            self.printed = character

    @property
    def text_x(self):
        return col_to_text_x(self.col)

    @property
    def text_y(self):
        return row_to_text_y(self.row)

    @property
    def room(self):
        return (self.row // rows_per_room, self.col // cols_per_room)

    def render(self):
        if self.printed:
            # Transiently show the printed character.
            character = self.printed
            self.printed = None
        else:
            character = self.character
        ctx.fillText(character, self.text_x, self.text_y)
        if self.captured:
            ctx.fillText("▥", self.text_x, self.text_y)


def render():
    # Clear the canvas ready for redrawing.
    ctx.clearRect(0, 0, canvas_width, canvas_height)

    # Render the room.
    render_room()

    # Render the grid.
    render_grid()

    # Render the agents.
    agent_foo.render()
    agent_bar.render()
    agent_plane.render()

    # Render the player.
    player.render()

    # Render the clue.
    render_clue()

    # Render the debug panel below the screen.
    moves_str = "".join(player.moves)
    moves_node.innerHTML = f'"{moves_str}"'
    position_node.innerHTML = (
        f'"{player.character}" at row {player.row}, col {player.col}'
    )
    speed_node.innerHTML = f"{speed} moves per second"


def render_grid():
    ctx.lineWidth = 1
    ctx.strokeStyle = "#bbb"
    for i in range(cols_per_room + 1):
        x = i * cell_width
        if x == 0:
            x += 0.5
        else:
            x -= 0.5
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas_height)
        ctx.stroke()
    for j in range(rows_per_room + 1):
        y = j * cell_width
        if y == 0:
            y += 0.5
        else:
            y -= 0.5
        ctx.beginPath()
        ctx.moveTo(0, y)
        ctx.lineTo(canvas_width, y)
        ctx.stroke()


def render_room():
    # Figure out which room the player is in and render that.
    row_offset = (player.row // rows_per_room) * rows_per_room
    col_offset = (player.col // cols_per_room) * cols_per_room
    for row in range(row_offset, row_offset + rows_per_room):
        for col in range(col_offset, col_offset + cols_per_room):
            if player.row == row and player.col == col:
                pass
            else:
                character = world[row][col]
                x = col_to_text_x(col)
                y = row_to_text_y(row)
                ctx.fillStyle = "black"
                ctx.fillText(character, x, y)


def render_clue():
    # Put the clue.
    i = player.row // rows_per_room
    j = player.col // cols_per_room
    clue = clues[i][j]
    if i == 0 and j == 0:
        trans = transformations[:1]
    elif i == 0 and j == 1:
        trans = transformations[:2]
    elif i == 0 and j == 2:
        trans = transformations[:3]
    elif i == 1 and j == 2:
        trans = transformations[:4]
    elif i == 1 and j == 1:
        trans = transformations[:5]
    elif i == 1 and j == 0:
        trans = transformations[:6]
    elif i == 2 and j == 0:
        trans = transformations[:7]
    elif i == 2 and j == 1:
        trans = transformations[:8]
    else:
        trans = transformations
    if clue:
        show(clue_container_node)
        original_clue = clue
        # Apply replacements.
        for row, col, character in trans:
            printed = world[row][col]
            clue = clue.replace(character, printed)
        content = f'"{clue}"'
        if clue == original_clue:
            content += " ✅"
        clue_node.innerHTML = content
    else:
        hide(clue_container_node)
        clue_node.innerHTML = ""


async def main():
    global canvas_node
    global canvas_width
    global canvas_height
    global ctx
    global cell_width
    global cell_height
    global world
    global clues
    global player
    global agent_foo
    global agent_bar
    global agent_plane

    hide(loading_node)
    terminal_node.style.visibility = "visible"

    # Initialise communication with the terminal worker.
    terminal_script_node = document.querySelector("script[terminal]")
    terminal_worker = terminal_script_node.xworker
    terminal_worker.sync.move = move_command
    terminal_worker.sync.change = change_command
    terminal_worker.sync.print = print_command
    terminal_worker.sync.speed = speed_command
    terminal_worker.sync.escape = escape_command

    # Set up canvas.
    canvas_width = min(canvas_container_node.offsetWidth, 400)
    # Round to nearest multiple of 10.
    canvas_width = canvas_width - (canvas_width % 10)
    canvas_height = canvas_width
    canvas_node = document.createElement("canvas")
    canvas_node.id = "canvas"
    canvas_node.width = canvas_width
    canvas_node.height = canvas_height
    canvas_container_node.appendChild(canvas_node)
    ctx = canvas_node.getContext("2d")
    cell_width = canvas_width // cols_per_room
    cell_height = canvas_height // rows_per_room

    # Fix visibility.
    show(info_node)

    # Set some invariant text rendering settings.
    ctx.textRendering = "optimizeLegibility"
    ctx.font = f"{cell_width*0.7}px 'Special Elite'"
    ctx.textAlign = "center"
    ctx.textBaseline = "middle"

    # Read world data.
    with open("world.csv", newline="") as f:
        world = list(csv.reader(f))

    # Read clues.
    with open("clues.csv", newline="") as f:
        clues = list(csv.reader(f))

    # Create player.
    player = Player(row=5, col=5)

    # Create agents.
    agent_foo = Agent(row=1, col=21, character="🕴🏼", recognition=25)
    agent_plane = Agent(row=11, col=21, character="🛩️", recognition=25)
    agent_bar = Agent(row=11, col=1, character="🕴🏼", recognition=25)

    # Start the game loop.
    moves = 0
    while True:
        await asyncio.sleep(1 / speed)
        player.move()
        # Agents move slower, every other frame.
        if moves % 2 == 0:
            agent_foo.move()
            agent_plane.move()
            agent_bar.move()
        render()
        if player.col >= 30:
            # Reached the hidden room, exit game loop.
            break
        moves += 1

    hide(info_node)
    hide(screen_node)
    show(outro_node)
    await html_speak(
        "outro",
        """\
⏸⏸Wait a minute, where are we? I've never seen this room before.

And is that a message? But — it's addressed to me. How can that be?

There's something very fishy going on here darling!

I thought we were fixing a broken compositor, but we seem to have unlocked a hidden room.

And apparently, I have a secret inside me!

I'm not sure about that, the only thing inside me are rusty circuits!

Anyway, well done darling, we've fixed the first compositor.

Let's keep going, at least we can recover some more of my script memory.

I wonder what else we'll find?
""",
    )
    hide(canvas_container_node)
    show(success_node)


if __name__ == "__main__":
    # Run the main function asynchronously to avoid blocking the
    # browser loop.
    js.setTimeout(create_proxy(main), 0)
