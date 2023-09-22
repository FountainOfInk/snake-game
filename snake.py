import time
import curses
import random

left, right, up, down = 0, 1, 2, 3

xoffset = {
    left: -1,
    right: 1,
    up: 0,
    down: 0
}
yoffset = {
    up: -1,
    down: 1,
    right: 0,
    left: 0
}
keytodir = {
    curses.KEY_LEFT: left,
    curses.KEY_RIGHT: right,
    curses.KEY_UP: up,
    curses.KEY_DOWN: down
}
dirtohead = {
    left: "<",
    right: ">",
    up: "^",
    down: "v"
}


class GameOver(Exception):
    pass


def shiftArray(a):
    for i in range(len(a)-1, 0, -1):
        a[i] = a[i-1].copy()        # python moment
    return a


def main(win):
    curses.curs_set(False)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    win.nodelay(True)

    cols, lines = curses.COLS, curses.LINES
    snake = [ [int(cols/2), int(lines/2)] ]
    appleX, appleY = random.randint(0, cols-1), random.randint(0, lines-1)

    direction = right

    while True:
        win.clear()

        inpt = win.getch()
        if inpt != curses.ERR:
            inpt = keytodir[inpt]
            if xoffset[direction] + xoffset[inpt] == 0 and yoffset[direction] + yoffset[inpt] == 0 and len(snake) > 1:
                pass            # Don't change direction if it's the exact opposite (left -> right, up -> down)
            else:
                direction = inpt

        shiftArray(snake)

        snake[0][0] += xoffset[direction]
        snake[0][1] += yoffset[direction]

        if snake[0] in snake[1:]:
            raise GameOver("poopy")

        for i, [snakeX, snakeY] in enumerate(snake):
            if i == 0:
                win.addch(snakeY, snakeX, dirtohead[direction], curses.color_pair(1))
                continue
            win.addch(snakeY, snakeX, "S", curses.color_pair(2))

        win.addch(appleY, appleX, "o", curses.color_pair(3))

        if appleX == snake[0][0] and appleY == snake[0][1]:
            snake.append([snake[-1][0] - xoffset[direction],
                          snake[-1][1] - yoffset[direction]])
            appleX, appleY = random.randint(0, cols-1), random.randint(0, lines-1)

        win.refresh()
        time.sleep(0.08)


curses.wrapper(main)
