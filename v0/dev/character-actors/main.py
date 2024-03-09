from collections import deque
import random
from util import (
    get_element_by_id,
    hide,
)
from pyscript import document
import js
from pyodide.ffi import create_proxy
import asyncio


screen_node = get_element_by_id("screen")
canvas_container_node = get_element_by_id("canvas_container")
loading_node = get_element_by_id("loading")
success_node = get_element_by_id("success")
moves_node = get_element_by_id("moves")
position_node = get_element_by_id("position")
speed_node = get_element_by_id("speed")
speed = 4
rows = 10
cols = 10
default_player_character = "🕵️"
people_emojis = [
    "👶",
    "🧒",
    "👦",
    "👧",
    "🧑",
    "👱",
    "👨",
    "🧔",
    "🧔‍♂️",
    "🧔‍♀️",
    "👨‍🦰",
    "👨‍🦱",
    "👨‍🦳",
    "👨‍🦲",
    "👩",
    "👩‍🦰",
    "🧑‍🦰",
    "👩‍🦱",
    "🧑",
    "🧑‍🦱",
    "👩‍🦳",
    "🧑‍🦳",
    "👩‍🦲",
    "🧑‍🦲",
    "👱‍♀️",
    "👱‍♂️",
    "🧓",
    "👴",
    "👵",
    "👳",
    "👳‍♂️",
    "👳‍♀️",
    "👲",
    "🧕",
    "👼",
]
role_emojis = [
    "🧑‍⚕️",
    "👨‍⚕️",
    "👩‍⚕️",
    "🧑‍🎓",
    "👨‍🎓",
    "👩‍🎓",
    "🧑‍🏫",
    "👨‍🏫",
    "👩‍🏫",
    "🧑‍⚖️",
    "👨‍⚖️",
    "👩‍⚖️",
    "🧑‍🌾",
    "👨‍🌾",
    "👩‍🌾",
    "🧑‍🍳",
    "👨‍🍳",
    "👩‍🍳",
    "🧑‍🔧",
    "👨‍🔧",
    "👩‍🔧",
    "🧑‍🏭",
    "👨‍🏭",
    "👩‍🏭",
    "🧑‍💼",
    "👨‍💼",
    "👩‍💼",
    "🧑‍🔬",
    "👨‍🔬",
    "👩‍🔬",
    "🧑‍💻",
    "👨‍💻",
    "👩‍💻",
    "🧑‍🎤",
    "👨‍🎤",
    "👩‍🎤",
    "🧑‍🎨",
    "👨‍🎨",
    "👩‍🎨",
    "🧑‍✈️",
    "👨‍✈️",
    "🧑‍🚀",
    "👨‍🚀",
    "👩‍🚀",
    "🧑‍🚒",
    "👨‍🚒",
    "👩‍🚒",
    "👮",
    "👮‍♂️",
    "👮‍♀️",
    "🕵️",
    "🕵️‍♂️",
    "🕵️‍♀️",
    "💂",
    "💂‍♂️",
    "💂‍♀️",
    "🥷",
    "👷",
    "👷‍♂️",
    "👷‍♀️",
    "🫅",
    "🤴",
    "👸",
    "🤵",
    "🤵‍♂️",
    "🤵‍♀️",
    "👰",
    "👰‍♂️",
    "👰‍♀️",
    "🎅",
    "🤶",
    "🧑‍🎄",
    "🦸",
    "🦸‍♂️",
    "🦸‍♀️",
    "🦹",
    "🦹‍♂️",
    "🦹‍♀️",
    "🧙",
    "🧙‍♂️",
    "🧙‍♀️",
    "🧚",
    "🧚‍♂️",
    "🧚‍♀️",
    "🧛",
    "🧛‍♂️",
    "🧛‍♀️",
    "🧜",
    "🧜‍♂️",
    "🧜‍♀️",
    "🧝",
    "🧝‍♀️",
    "🧞",
    "🧞‍♂️",
    "🧞‍♀️",
    "🧟",
    "🧟‍♂️",
    "🧟‍♀️",
    "🧌",
]
mammal_emojis = [
    "🐵",
    "🐒",
    "🦍",
    "🦧",
    "🐶",
    "🐕",
    "🦮",
    "🐩",
    "🐺",
    "🦊",
    "🦝",
    "🐱",
    "🐈",
    "🦁",
    "🐯",
    "🐅",
    "🐆",
    "🐴",
    "🫎",
    "🫏",
    "🐎",
    "🦄",
    "🦓",
    "🦌",
    "🦬",
    "🐮",
    "🐂",
    "🐃",
    "🐄",
    "🐷",
    "🐖",
    "🐗",
    "🐽",
    "🐏",
    "🐑",
    "🐐",
    "🐪",
    "🐫",
    "🦙",
    "🦒",
    "🐘",
    "🦣",
    "🦏",
    "🦛",
    "🐭",
    "🐁",
    "🐀",
    "🐹",
    "🐰",
    "🐇",
    "🐿️",
    "🦫",
    "🦔",
    "🦇",
    "🐻",
    "🐻‍❄️",
    "🐨",
    "🐼",
    "🦥",
    "🦦",
    "🦨",
    "🦘",
    "🦡",
]
bird_emojis = [
    "🦃",
    "🐔",
    "🐓",
    "🐣",
    "🐤",
    "🐥",
    "🐦",
    "🐧",
    "🕊️",
    "🦅",
    "🦆",
    "🦢",
    "🦉",
    "🦤",
    "🦩",
    "🦚",
    "🦜",
    "🐦‍⬛",
    "🪿",
]
reptile_emojis = ["🐸", "🐊", "🐢", "🦎", "🐍", "🐲", "🐉", "🦕", "🦖"]
marine_emojis = [
    "🐳",
    "🐋",
    "🐬",
    "🦭",
    "🐟",
    "🐠",
    "🐡",
    "🦈",
    "🐙",
    "🐚",
    "🪸",
    "🪼",
    "🦀",
    "🦞",
    "🦐",
    "🦑",
    "🦪",
]
bug_emojis = [
    "🐌",
    "🦋",
    "🐛",
    "🐜",
    "🐝",
    "🪲",
    "🐞",
    "🦗",
    "🪳",
    "🕷️",
    "🦂",
    "🦟",
    "🪰",
    "🪱",
    "🦠",
]
disguises = (
    people_emojis
    + role_emojis
    + mammal_emojis
    + bird_emojis
    + reptile_emojis
    + marine_emojis
    + bug_emojis
)
block_chars = ["⬜", "🟥", "🟦", "🟩", "🟨", "🟧", "🟪", "🟫", "⬛", "🔲"]


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
    room[player.row][player.col] = character


def col_to_x(col):
    return (col * cell_size) + (cell_size / 2)


def row_to_y(row):
    return (row * cell_size) + (cell_size / 2) + 3


class Player:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.character = default_player_character
        self.moves = deque()

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

            # Out of bounds checks.
            if new_row < 0:
                return
            if new_row > rows - 1:
                return
            if new_col < 0:
                return
            if new_col > cols - 1:
                return

            # Stop checks.
            new_char = room[new_row][new_col]
            if new_char in block_chars:
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
        ctx.fillText(self.character, self.x, self.y)


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
    moves_node.innerHTML = "".join(player.moves)
    position_node.innerHTML = (
        f'"{player.character}" at row {player.col}, col {player.row}'
    )
    speed_node.innerHTML = f"{speed} FPS"


def render_grid():
    ctx.lineWidth = 1
    ctx.strokeStyle = "#555"
    for i in range(cols + 1):
        x = i * cell_size
        if x == 0:
            x += 0.5
        else:
            x -= 0.5
        ctx.beginPath()
        ctx.moveTo(x, 0)
        ctx.lineTo(x, canvas_height)
        ctx.stroke()
    for j in range(rows + 1):
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
    for row in range(rows):
        for col in range(cols):
            if player.row == row and player.col == col:
                pass
            else:
                character = room[row][col]
                if character == ".":
                    x = col * cell_size
                    y = row * cell_size
                    ctx.fillStyle = "#ccc"
                    ctx.fillRect(x, y, cell_size, cell_size)
                else:
                    x = col_to_x(col)
                    y = row_to_y(row)
                    ctx.fillStyle = "black"
                    ctx.fillText(character, x, y)


async def main():
    global canvas_node
    global canvas_width
    global canvas_height
    global ctx
    global cell_size
    global rooms
    global room
    global player

    hide(loading_node)

    # Initialise communication with the terminal.
    terminal_script_node = document.querySelector("script[terminal]")
    terminal_worker = terminal_script_node.xworker
    terminal_worker.sync.add_moves = add_moves
    terminal_worker.sync.change_character = change_character
    terminal_worker.sync.print_character = print_character
    terminal_worker.sync.set_speed = set_speed

    # Set up canvas.
    canvas_width = min(canvas_container_node.offsetWidth, 500)
    # Round to nearest multiple of 10.
    canvas_width = canvas_width - (canvas_width % 10)
    canvas_height = canvas_width
    canvas_node = document.createElement("canvas")
    canvas_node.id = "canvas"
    canvas_node.width = canvas_width
    canvas_node.height = canvas_height
    canvas_container_node.appendChild(canvas_node)
    ctx = canvas_node.getContext("2d")
    cell_size = canvas_width // 10

    # Set some invariant text rendering settings.
    ctx.textRendering = "optimizeLegibility"
    ctx.font = f"{cell_size*0.7}px 'Special Elite'"
    ctx.textAlign = "center"
    ctx.textBaseline = "middle"

    # Read room data.
    with open("rooms.csv") as f:
        room_data = [line.split(",") for line in f.readlines()]
    rooms = [[[line[:10] for line in room_data[:10]]]]
    room = rooms[0][0]

    # Create player.
    player = Player(col=5, row=5)

    # Start the game loop.
    while True:
        await asyncio.sleep(1 / speed)
        player.move()
        render()


if __name__ == "__main__":
    # Run the main function asynchronously to avoid blocking the
    # browser loop.
    js.setTimeout(create_proxy(main), 0)
