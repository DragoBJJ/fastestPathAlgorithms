import curses
from curses import wrapper
import queue
import _testimportmultiple
import time

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


def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)
    GREEN = curses.color_pair(3)

    for i,row in enumerate(maze):
        for j, col in enumerate(row):
            if (i,j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                if col == "X":
                    stdscr.addstr(i, j*2, col, GREEN)
                else:    
                    stdscr.addstr(i, j*2, col, BLUE)


def find_start(maze, start):
      for i, row in enumerate(maze):
          for j, col in enumerate(row):
              if col == start:
                  return i, j
      return None



def find_path(maze, stdscr):
    start = "O"
    end = "X"

    start_position = find_start(maze, start)

    q = queue.Queue()
    q.put((start_position, [start_position]))

    visited_postion = set()

    while not q.empty():
        start_position, current_path = q.get()

        ## Get last item from the queue
        row, col = start_position


        stdscr.clear()
        print_maze(maze,stdscr, current_path)
        time.sleep(0.2)
        stdscr.refresh()
        
        if maze[row][col] == end:
            return current_path
        
        neighbors = find_neighbors(maze, row, col)

        for neighbor in neighbors:

            if neighbor in visited_postion:
                 continue
            
            r,c = neighbor

            if maze[r][c] == "#":
                   continue
               
            new_path = current_path + [neighbor]
            q.put((neighbor, new_path))
            visited_postion.add(neighbor)
                
                   
             
        

def find_neighbors(maze, row, col):       
    neighbors = []

    if row > 0:
       neighbors.append((row-1, col))
    
    if row + 1 < len(maze):
        neighbors.append((row + 1, col))
    
    if col > 0:
        neighbors.append((row, col - 1))
    
    if col + 1 < len(maze[0]):
       neighbors.append((row, col + 1)) 
    
    return neighbors




def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    print_maze(maze, stdscr)
    find_path(maze, stdscr)
    stdscr.getch()

wrapper(main)