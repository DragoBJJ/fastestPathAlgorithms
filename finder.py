import curses
import time
from curses import wrapper
from queue import Queue


maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def init_game_color():
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)


def get_game_color():
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)
    GREEN = curses.color_pair(3)
    return ((BLUE, RED, GREEN))


def start_drawing(maze, stdscr, current_path):
    stdscr.clear()
    print_maze(maze, stdscr, current_path)
    time.sleep(0.2)
    stdscr.refresh()


def find_neighbors(maze_lenght, current_point):
    neighbors = []
    row, col = current_point

    if row > 0:
        neighbors.append((row - 1, col))
    if row + 1 < maze_lenght:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))

    return neighbors


def find_start_point(maze, start_alias):
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == start_alias:
                return i, j
    return None


def neighbords_logic(q, current_point, current_path, visited_position):

    neighbors = find_neighbors(len(maze), current_point)

    for neighbor in neighbors:

        if neighbor in visited_position:
            continue

        r, c = neighbor
        if maze[r][c] == "#":
            continue

        new_path = current_path + [neighbor]
        q.put((neighbor, new_path))
        visited_position.add(neighbor)


def maze_logic(maze, stdscr):
    start_alias = "O"
    end_alias = "X"

    start_point = find_start_point(maze, start_alias)

    q = Queue()
    visited_position = set()

    q.put((start_point, [start_point]))

    while not q.empty():
        current_point, current_path = q.get()

        start_drawing(maze, stdscr, current_path)
        row, col = current_point

        if maze[row][col] == end_alias:
            stdscr.getch()
            return

        neighbords_logic(q, current_point, current_path, visited_position)


def print_maze(maze, stdscr, current_path=[]):
    BLUE, RED, GREEN = get_game_color()

    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if (i, j) in current_path:
                stdscr.addstr(i, j * 2, "X", BLUE)
            else:
                if col == "X":
                    stdscr.addstr(i, j * 2, col, GREEN)
                else:
                    stdscr.addstr(i, j * 2, col, RED)


def main(stdscr):
    init_game_color()
    print_maze(maze, stdscr)
    maze_logic(maze, stdscr)


wrapper(main)
