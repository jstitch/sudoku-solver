"""
9x9 Sudoku solver

Licensed under the GPLv3
"""

import sys
import curses
import time

row = ['.'] * 9
puzzle = [row[:] for i in range(0,9)]

# test sudoku from http://upload.wikimedia.org/wikipedia/commons/f/ff/Sudoku-by-L2G-20050714.svg
# answer at http://upload.wikimedia.org/wikipedia/commons/3/31/Sudoku-by-L2G-20050714_solution.svg
# puzzle[0][0] = -5
# puzzle[0][1] = -3
# puzzle[0][4] = -7
# puzzle[1][0] = -6
# puzzle[1][3] = -1
# puzzle[1][4] = -9
# puzzle[1][5] = -5
# puzzle[2][1] = -9
# puzzle[2][2] = -8
# puzzle[2][7] = -6
# puzzle[3][0] = -8
# puzzle[3][4] = -6
# puzzle[3][8] = -3
# puzzle[4][0] = -4
# puzzle[4][3] = -8
# puzzle[4][5] = -3
# puzzle[4][8] = -1
# puzzle[5][0] = -7
# puzzle[5][4] = -2
# puzzle[5][8] = -6
# puzzle[6][1] = -6
# puzzle[6][6] = -2
# puzzle[6][7] = -8
# puzzle[7][3] = -4
# puzzle[7][4] = -1
# puzzle[7][5] = -9
# puzzle[7][8] = -5
# puzzle[8][4] = -8
# puzzle[8][7] = -7
# puzzle[8][8] = -9

# UI, setup puzzle from file
def initpuzzle (file, puzle = []):
    """
    Setups the sudoku puzzle to solve from certain text file
    """
    f = open(file, 'r')
    for r, row in enumerate(f):
        for c, cell in enumerate(row):
            if cell == '\n': continue
            try:
                int(cell)
                puzzle[r][c] = -1 * int(cell)
            except Exception as e:
                puzzle[r][c] = '.'
    f.close()

# UI, print a puzzle sample. Also may print to file
def printpuzzle (puzle = [], f = None):
    """
    Prints puzzle in current status, using curses

    It may print in to a file too
    """
    global scr
    for r, row in enumerate(puzzle):
        for c, cell in enumerate(row):
            if cell == '.':
                scr.addstr(r*3, c*3, str(cell))
                if f != None: f.write(str(cell))
            else:
                scr.addstr(r*3, c*3, str(abs(int(cell))))
                if f != None: f.write(str(abs(int(cell))))
        if f != None: f.write('\n')
    scr.refresh()
    time.sleep(0.0)

# UI, main routine, calling certain sudoku solver routine
def solvesudoku (file, puzle = []) :
    """
    Main routine which seeks the sudoku solving.

    Uses curses to print in screen
    """
    global scr
    initpuzzle(file, puzzle)
    printpuzzle(puzle)
    r = nextsquare((0,0), puzle)
    f = open(file + "_solved", 'w')
    if r == -1:
        scr.addstr(25, 0, "No solution found!")
        f.write("No solution found!\n")
        printpuzzle(puzle)
    else:
        printpuzzle(puzle, f)
    f.close()
    c = scr.getch()

# Brute force recursive algorithm
def nextsquare ((x, y), puzle = []):
    """
    Recursive algorithm to solve sudoku puzzle, via brute-force
    """
    if (x, y) == (-1, -1):
        return 1

    if puzle[x][y] == '.':
        for val in range(1, 10):
            valid = validate((x, y), val, puzle)
            if valid:
                puzle[x][y] = val
                printpuzzle(puzle)
                r = nextsquare(nextcoords(x, y), puzle)
                if r == 1:
                    return 1

        puzle[x][y] = '.'
        printpuzzle(puzle)
        return -1

    elif puzle[x][y] < 0 or puzle[x][y] > 0:
        r = nextsquare(nextcoords(x, y), puzle)
        if r == 1:
            return 1

    return -1


# Brute force recursive algorithm, get next coordinates in recursiveness
def nextcoords (x = 0, y = 0):
    """
    Gets the next pair of coordinates for the brute force recursive algorithm
    """
    y = y + 1
    if y == 9:
        y = 0
        x = x + 1
        if x == 9:
            return (-1, -1)

    return (x, y)

# Sudoku solver, validate new value in certain coordinates
def validate ((x, y), val, puzle = []):
    """
    Given some value at certain coordinates, validates according to sudoku rules
    """
    # valida renglones
    for v in puzle[x]:
        if v == '.': continue
        if abs(int(v)) == val:
            return False

    # valida columnas
    ycol = [row[y] for row in puzle]
    for v in [cv for cv in ycol]:
        if v == '.': continue
        if abs(int(v)) == val:
            return False

    # valida cuadrantes
    X = x / 3 # cuadrante en X
    Y = y / 3 # cuadrante en Y

    for i in range(1,10):
        if i / 3 != X: continue
        for j in range(1,10):
            if j / 3 != Y: continue
            v = puzle[i][j]
            if v == '.': continue
            if abs(int(v)) == val:
                return False

    return True

# Rutina principal
if __name__ == '__main__':
    global scr

    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.curs_set(0)
    scr.keypad(1)

    try:
        filename = sys.argv[1]
    except Exception as e:
        filename = 'sudoku_test'
    try:
        solvesudoku(filename, puzzle[:])
    except KeyboardInterrupt:
        pass
    except Exception as e:
        scr.addstr("Error! " + str(e))
        scr.refresh()
        scr.getch()
        pass

    curses.nocbreak()
    curses.echo()
    curses.endwin()
