import curses
from curses import wrapper
import time
import queue

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "O", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", " ", "#", "#", "#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", " ", "#", "#", "#", " ", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#", "#", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", " ", "#", "#", "#", " ", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "X", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]


def draw_maze(stdscr, maze, path=[]):
    stdscr.clear()

    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            char = cell
            color = curses.color_pair(1)

            if cell == "#":
                color = curses.color_pair(2)   # Wall
            elif cell == "O":
                color = curses.color_pair(3)   # Start
            elif cell == "X":
                color = curses.color_pair(4)   # End
            elif (i, j) in path:
                char = "*"
                color = curses.color_pair(5)   # Path

            stdscr.addstr(i, j * 2, char, color)

    stdscr.refresh()

def find_start(maze):
    for i, row in enumerate(maze):     
        for j, val in enumerate(row):
            if val == "O":
                return i, j
    return None

def find_neighbors(maze, row, col):
    neighbors = []
    if row > 0: neighbors.append((row - 1, col))
    if row < len(maze) - 1: neighbors.append((row + 1, col))
    if col > 0: neighbors.append((row, col - 1))
    if col < len(maze[0]) - 1: neighbors.append((row, col + 1))
    return neighbors

def bfs(stdscr, maze):
    start = find_start(maze)
    q = queue.Queue() # for tupple and list comb -> [start_pos] = path 2nd element
    q.put((start, [start]))
    # to grown the path will track by like indexing (start_pos -> pos 1st element


    visited = set()

    while not q.empty():
        current, path = q.get()
        row, col = current

        draw_maze(stdscr, maze, path) # path is default arg
        #stdscr.addstr(0 ,0 , "hello yash" , black_and_blue)#  arg list 
        time.sleep(0.15)

        if maze[row][col] == "X":
            return path

        for neighbor in find_neighbors(maze, row, col):
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            visited.add(neighbor)
            q.put((neighbor, path + [neighbor]))  # tracking the neighbor at current path 

def main(stdscr):# arg -> std output screen

    curses.curs_set(0)
    curses.start_color()

    # Color pairs (optimized for dark terminal)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Default  id -> 1
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Walls
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Start
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)     # End
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Path

    bfs(stdscr, maze)
    stdscr.addstr(len(maze) + 1, 0, "✔ Path Found! Press any key to exit.")
    stdscr.getch()

wrapper(main)
