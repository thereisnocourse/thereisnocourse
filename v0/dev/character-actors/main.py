from collections import deque
import random
import csv
from util import (
    get_element_by_id,
    hide,
    show,
)
from pyscript import document
import js
from pyodide.ffi import create_proxy
import asyncio
import emoji


terminal_node = get_element_by_id("terminal")
canvas_container_node = get_element_by_id("canvas_container")
loading_node = get_element_by_id("loading")
success_node = get_element_by_id("success")
clue_node = get_element_by_id("clue")
clue_container_node = get_element_by_id("clue_container")
moves_node = get_element_by_id("moves")
position_node = get_element_by_id("position")
speed_node = get_element_by_id("speed")
speed = 4
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


def set_speed(new_speed):
    global speed
    speed = new_speed


def add_moves(moves):
    player.add_moves(moves)


def change_character(*args):
    if len(args) == 0:
        player.change()
    elif len(args) == 1:
        character = args[0]
        player.change(character)


def print_character(character):
    if not isinstance(character, str):
        raise TypeError
    if len(character) != 1:
        raise ValueError
    world[player.row][player.col] = character
    player.printed = character

    # Check to see if all replacements have been solved.
    solved = True
    for row, col, character in transformations:
        printed = world[row][col]
        solved = solved and (character == printed)
    if solved:
        world[28][29] = ""
    else:
        world[28][29] = "🔒"


def col_to_x(col):
    return ((col % cols_per_room) * cell_size) + (cell_size / 2)


def row_to_y(row):
    return ((row % rows_per_room) * cell_size) + (cell_size / 2) + 3


class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.character = default_player_character
        self.moves = deque()
        self.printed = None

    def add_moves(self, moves):
        self.moves.extend(list(moves.lower()))

    def move(self):
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
            if new_char in (emoji.blocks + ["🔒"]):
                return

            self.row = new_row
            self.col = new_col

    def change(self, character=None):
        if character is None:
            self.character = random.choice(disguises)
        else:
            if not isinstance(character, str):
                raise TypeError
            self.character = character

    @property
    def x(self):
        return col_to_x(self.col)

    @property
    def y(self):
        return row_to_y(self.row)

    def render(self):
        if self.printed:
            # Transiently show the printed character.
            character = self.printed
            self.printed = None
        else:
            character = self.character
        ctx.fillText(character, self.x, self.y)


def render():
    # Clear the canvas ready for redrawing.
    ctx.clearRect(0, 0, canvas_width, canvas_height)

    # Render the room.
    render_room()

    # Render the grid.
    render_grid()

    # Render the player.
    player.render()

    # Render the debug panel below the screen.
    moves_str = "".join(player.moves)
    moves_node.innerHTML = f'"{moves_str}"'
    position_node.innerHTML = (
        f'"{player.character}" at row {player.row}, col {player.col}'
    )
    speed_node.innerHTML = f"{speed} FPS"


def render_grid():
    ctx.lineWidth = 1
    ctx.strokeStyle = "#bbb"
    for i in range(cols_per_room + 1):
        x = i * cell_size
        if x == 0:
            x += 0.5
        else:
            x -= 0.5
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas_height)
        ctx.stroke()
    for j in range(rows_per_room + 1):
        y = j * cell_size
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
                x = col_to_x(col)
                y = row_to_y(row)
                ctx.fillStyle = "black"
                ctx.fillText(character, x, y)
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
    global cell_size
    global world
    global clues
    global player

    hide(loading_node)
    terminal_node.style.visibility = "visible"

    # Initialise communication with the terminal.
    terminal_script_node = document.querySelector("script[terminal]")
    terminal_worker = terminal_script_node.xworker
    terminal_worker.sync.add_moves = add_moves
    terminal_worker.sync.change_character = change_character
    terminal_worker.sync.print_character = print_character
    terminal_worker.sync.set_speed = set_speed

    # Set up canvas.
    canvas_width = min(canvas_container_node.offsetWidth, 450)
    # Round to nearest multiple of 10.
    canvas_width = canvas_width - (canvas_width % 10)
    canvas_height = canvas_width
    canvas_node = document.createElement("canvas")
    canvas_node.id = "canvas"
    canvas_node.width = canvas_width
    canvas_node.height = canvas_height
    canvas_container_node.appendChild(canvas_node)
    ctx = canvas_node.getContext("2d")
    cell_size = canvas_width // rows_per_room

    # Set some invariant text rendering settings.
    ctx.textRendering = "optimizeLegibility"
    ctx.font = f"{cell_size*0.7}px 'Special Elite'"
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

    # Start the game loop.
    while True:
        await asyncio.sleep(1 / speed)
        player.move()
        render()


if __name__ == "__main__":
    # Run the main function asynchronously to avoid blocking the
    # browser loop.
    js.setTimeout(create_proxy(main), 0)
