import curses #pip install windows_curses
from curses import wrapper
import time
import random

def start_screen(stdscrs):
    stdscrs.clear()
    stdscrs.addstr("Welcome to the Speed Typing) Test!")
    stdscrs.addstr("\nPress any key to begin!")
    stdscrs.refresh()
    stdscrs.getkey()

def display_text(stdscrs,target, current, wpm=0):
        stdscrs.addstr(target)
        stdscrs.addstr(3, 0, f"WPM: {wpm}")

        for i, char in enumerate(current):
            correct_char = target[i]
            color = curses.color_pair(1)
            if char != correct_char:
                color = curses.color_pair(2)

            stdscrs.addstr(0, i, char,color )

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        line = random.choice(lines).strip()

    return line

def wpm_test(stdscrs):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscrs.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time,1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscrs.clear()

        display_text(stdscrs, target_text, current_text, wpm)

        stdscrs.refresh()

        if "".join(current_text) == target_text:
            stdscrs.nodelay(False)
            break

        try:
            key = stdscrs.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)



def main(stdscrs):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscrs)

    while True:
        wpm_test(stdscrs)
        stdscrs.addstr(4,0, "You completed the text! Press any key to continue...")
        key = stdscrs.getkey()

        if ord(key) == 27:
            break

wrapper(main)
