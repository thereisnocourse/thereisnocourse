from collections import deque
from util import (
    get_element_by_id,
    hide,
)
from pyscript import document
import js
from pyodide.ffi import create_proxy
import asyncio


loading_node = get_element_by_id("loading")
success_node = get_element_by_id("success")
canvas_node = get_element_by_id("canvas")
moves_node = get_element_by_id("moves")
position_node = get_element_by_id("position")
canvas_width = canvas_node.width
canvas_height = canvas_node.height
ctx = canvas_node.getContext("2d")
cell_size = 40
player_x = None
player_y = None
moves_queue = deque()
default_player_character = "🕵️"
player_character = default_player_character


def add_moves(moves):
    moves_queue.extend(list(moves.lower()))
    render()


def change_character(*args):
    global player_character
    if len(args) == 0:
        player_character = default_player_character
        # TODO randomly pick a disguise
        render()
    elif len(args) == 1:
        character = args[0]
        if isinstance(character, str) and len(character) == 1:
            player_character = character
            render()


def render():
    ctx.clearRect(0, 0, canvas_width, canvas_height)
    moves_node.innerHTML = "".join(moves_queue)
    position_node.innerHTML = f"{player_character} [{player_x}, {player_y}]"

    ctx.lineWidth = 1
    ctx.strokeStyle = "#666"
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

    x = (player_x * cell_size) + (cell_size / 2)
    y = (player_y * cell_size) + (cell_size / 2) + 3
    ctx.textRendering = "optimizeLegibility"
    ctx.font = "28px 'Special Elite'"
    ctx.textAlign = "center"
    ctx.textBaseline = "middle"
    ctx.fillText(player_character, x, y)


def exec_move():
    global player_x, player_y, cols, rows
    try:
        move = moves_queue.popleft()
    except IndexError:
        pass
    else:
        # N.B., Y coords are from the top.
        if move == "d" and player_y < rows - 1:
            player_y += 1
        elif move == "u" and player_y > 0:
            player_y -= 1
        elif move == "r" and player_x < cols - 1:
            player_x += 1
        elif move == "l" and player_x > 0:
            player_x -= 1
        render()


async def main():
    hide(loading_node)
    global cols, rows, player_x, player_y

    cols = canvas_width // cell_size
    rows = canvas_height // cell_size

    player_x = cols // 2
    player_y = rows // 2
    render()

    terminal_script_node = document.querySelector("script[terminal]")
    terminal_worker = terminal_script_node.xworker
    terminal_worker.sync.add_moves = add_moves
    terminal_worker.sync.change_character = change_character

    while True:
        await asyncio.sleep(0.5)
        exec_move()


if __name__ == "__main__":
    js.setTimeout(create_proxy(main), 0)
