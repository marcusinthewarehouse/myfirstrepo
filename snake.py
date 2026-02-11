#!/usr/bin/env python3
"""Terminal Snake Game — play it right in your CLI!

Controls:
  Arrow keys or WASD to move
  P to pause/unpause
  Q to quit

Run:  python3 snake.py
"""

import curses
import random
import time

# Game settings
INITIAL_SPEED = 120        # ms per tick (lower = faster)
SPEED_INCREMENT = 2        # ms faster per food eaten
MIN_SPEED = 50             # fastest possible tick
BOARD_WIDTH = 40
BOARD_HEIGHT = 20


def main(stdscr):
    # ── Setup ────────────────────────────────────────────────────
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(INITIAL_SPEED)

    # Colours
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)   # snake body
    curses.init_pair(2, curses.COLOR_RED, -1)      # food
    curses.init_pair(3, curses.COLOR_YELLOW, -1)   # border / score
    curses.init_pair(4, curses.COLOR_CYAN, -1)     # head

    # Check terminal size
    max_y, max_x = stdscr.getmaxyx()
    needed_h = BOARD_HEIGHT + 4
    needed_w = BOARD_WIDTH + 4
    if max_y < needed_h or max_x < needed_w:
        stdscr.nodelay(False)
        stdscr.addstr(0, 0, f"Terminal too small! Need at least {needed_w}x{needed_h}.")
        stdscr.addstr(1, 0, "Resize and try again. Press any key to exit.")
        stdscr.getch()
        return

    # Offsets to centre the board
    off_y = (max_y - needed_h) // 2 + 1
    off_x = (max_x - needed_w) // 2

    # ── Game state ───────────────────────────────────────────────
    direction = curses.KEY_RIGHT
    snake = [(BOARD_HEIGHT // 2, BOARD_WIDTH // 4 + i) for i in range(3)]
    score = 0
    speed = INITIAL_SPEED
    paused = False

    def place_food():
        while True:
            fy = random.randint(1, BOARD_HEIGHT - 2)
            fx = random.randint(1, BOARD_WIDTH - 2)
            if (fy, fx) not in snake:
                return (fy, fx)

    food = place_food()

    def draw_border():
        for x in range(BOARD_WIDTH):
            stdscr.addch(off_y, off_x + x, curses.ACS_HLINE, curses.color_pair(3))
            stdscr.addch(off_y + BOARD_HEIGHT - 1, off_x + x, curses.ACS_HLINE, curses.color_pair(3))
        for y in range(BOARD_HEIGHT):
            stdscr.addch(off_y + y, off_x, curses.ACS_VLINE, curses.color_pair(3))
            stdscr.addch(off_y + y, off_x + BOARD_WIDTH - 1, curses.ACS_VLINE, curses.color_pair(3))
        # corners
        stdscr.addch(off_y, off_x, curses.ACS_ULCORNER, curses.color_pair(3))
        stdscr.addch(off_y, off_x + BOARD_WIDTH - 1, curses.ACS_URCORNER, curses.color_pair(3))
        stdscr.addch(off_y + BOARD_HEIGHT - 1, off_x, curses.ACS_LLCORNER, curses.color_pair(3))
        stdscr.addch(off_y + BOARD_HEIGHT - 1, off_x + BOARD_WIDTH - 1, curses.ACS_LRCORNER, curses.color_pair(3))

    def draw_score():
        label = f" Score: {score} "
        sx = off_x + (BOARD_WIDTH - len(label)) // 2
        stdscr.addstr(off_y - 1, sx, label, curses.color_pair(3) | curses.A_BOLD)

    def draw_help():
        help_text = "Arrow/WASD: Move | P: Pause | Q: Quit"
        hx = off_x + (BOARD_WIDTH - len(help_text)) // 2
        stdscr.addstr(off_y + BOARD_HEIGHT, hx, help_text, curses.color_pair(3))

    # Key mapping (WASD + arrows)
    KEY_MAP = {
        ord('w'): curses.KEY_UP,    ord('W'): curses.KEY_UP,
        ord('s'): curses.KEY_DOWN,  ord('S'): curses.KEY_DOWN,
        ord('a'): curses.KEY_LEFT,  ord('A'): curses.KEY_LEFT,
        ord('d'): curses.KEY_RIGHT, ord('D'): curses.KEY_RIGHT,
    }

    OPPOSITES = {
        curses.KEY_UP: curses.KEY_DOWN,
        curses.KEY_DOWN: curses.KEY_UP,
        curses.KEY_LEFT: curses.KEY_RIGHT,
        curses.KEY_RIGHT: curses.KEY_LEFT,
    }

    # ── Game loop ────────────────────────────────────────────────
    while True:
        stdscr.erase()

        # Input
        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            return
        if key in (ord('p'), ord('P')):
            paused = not paused
        if not paused:
            mapped = KEY_MAP.get(key, key)
            if mapped in OPPOSITES and mapped != OPPOSITES.get(direction):
                direction = mapped

        # Draw static elements
        draw_border()
        draw_score()
        draw_help()

        if paused:
            pause_msg = " PAUSED "
            px = off_x + (BOARD_WIDTH - len(pause_msg)) // 2
            py = off_y + BOARD_HEIGHT // 2
            stdscr.addstr(py, px, pause_msg, curses.color_pair(3) | curses.A_BOLD | curses.A_BLINK)
            stdscr.refresh()
            continue

        # Move snake
        head_y, head_x = snake[-1]
        if direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1

        new_head = (head_y, head_x)

        # Collision check — walls
        if head_y <= 0 or head_y >= BOARD_HEIGHT - 1 or head_x <= 0 or head_x >= BOARD_WIDTH - 1:
            break
        # Collision check — self
        if new_head in snake:
            break

        snake.append(new_head)

        # Eat food?
        if new_head == food:
            score += 1
            speed = max(MIN_SPEED, speed - SPEED_INCREMENT)
            stdscr.timeout(speed)
            food = place_food()
        else:
            snake.pop(0)

        # Draw food
        fy, fx = food
        stdscr.addstr(off_y + fy, off_x + fx, "*", curses.color_pair(2) | curses.A_BOLD)

        # Draw snake
        for i, (sy, sx) in enumerate(snake):
            if i == len(snake) - 1:
                stdscr.addstr(off_y + sy, off_x + sx, "@", curses.color_pair(4) | curses.A_BOLD)
            else:
                stdscr.addstr(off_y + sy, off_x + sx, "o", curses.color_pair(1))

        stdscr.refresh()

    # ── Game over ────────────────────────────────────────────────
    stdscr.nodelay(False)
    stdscr.timeout(-1)

    game_over_lines = [
        "╔══════════════════╗",
        "║    GAME  OVER    ║",
        f"║   Score: {score:<8}║",
        "║                  ║",
        "║  R to Restart    ║",
        "║  Q to Quit       ║",
        "╚══════════════════╝",
    ]

    box_h = len(game_over_lines)
    box_w = len(game_over_lines[0])
    by = off_y + (BOARD_HEIGHT - box_h) // 2
    bx = off_x + (BOARD_WIDTH - box_w) // 2

    for i, line in enumerate(game_over_lines):
        stdscr.addstr(by + i, bx, line, curses.color_pair(2) | curses.A_BOLD)
    stdscr.refresh()

    while True:
        ch = stdscr.getch()
        if ch in (ord('q'), ord('Q')):
            return
        if ch in (ord('r'), ord('R')):
            main(stdscr)  # restart
            return


if __name__ == "__main__":
    curses.wrapper(main)
