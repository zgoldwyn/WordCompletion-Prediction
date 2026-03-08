import re
import sys
sys.setrecursionlimit(10000)
import Trie
import NGram
import curses
import sqlite3
import pandas as pd
import os



def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # selected color
    selected = menu(stdscr)
    readfile = selected[0]
    readsql = selected[1]
    readcsv = selected[2]
    trainer = "mobydick.txt"
    ngram = NGram.NGram(4)
    trie = Trie.Trie()

    combo = f"{'f' if readfile else ''}{'s' if readsql else ''}{'c' if readcsv else ''}"
    TRIE_PATH = f"trie_{combo}.pkl"
    NGRAM_PATH = f"ngram_{combo}.pkl"
    stdscr.addstr(0, 0, f"Looking for: {TRIE_PATH}")
    stdscr.refresh()
    curses.napms(2000)

    if os.path.exists(TRIE_PATH) and os.path.exists(NGRAM_PATH):
        stdscr.addstr(0, 0, "Loading from cache...")
        stdscr.refresh()
        trie.load(TRIE_PATH)
        ngram.load(NGRAM_PATH)
    else:
        if readfile:
            stdscr.addstr(0, 0, "Loading Moby Dick...")
            stdscr.refresh()
            ngram.train(trainer)
            with open(trainer, "r") as f:
                for line in f:
                    a = line.split()
                    for word in a:
                        word = re.sub(r'[^a-zA-Z]', '', word)
                        word = word.lower()
                        trie.insert(word)
        if readsql:
            stdscr.addstr(0, 0, "Loading iMessages...  ")
            stdscr.refresh()
            conn = sqlite3.connect("chat.db")
            cursor = conn.cursor()
            cursor.execute("SELECT text FROM message WHERE text IS NOT NULL")
            messages = cursor.fetchall()
            ngram.train_from_messages(messages)
            for row in messages:
                text = row[0]
                for word in text.split():  # split on spaces first
                    word = re.sub(r'[^a-zA-Z]', '', word).lower()
                    if word:  # skip empty strings
                        trie.insert(word)
        if readcsv:
            stdscr.addstr(0, 0, "Loading Reddit...     ")
            stdscr.refresh()
            df = pd.read_csv("reddit_comments.csv")
            body = df['body']
            ngram.train_from_csv(body)
            for row in body:
                for word in row.split():  # split on spaces first
                    word = re.sub(r'[^a-zA-Z]', '', word).lower()
                    if word:  # skip empty strings
                        trie.insert(word)
        combo = f"{'f' if readfile else ''}{'s' if readsql else ''}{'c' if readcsv else ''}"
        TRIE_PATH = f"trie_{combo}.pkl"
        NGRAM_PATH = f"ngram_{combo}.pkl"
        stdscr.addstr(0, 0, "Saving to cache...    ")
        stdscr.refresh()
        trie.save(TRIE_PATH)
        ngram.save(NGRAM_PATH)
        # stdscr is screen object (draw to it)
    stdscr.clear()
    stdscr.addstr(0, 0, "Ready! Start typing. Press ESC to quit, TAB to accept suggestion.")
    stdscr.refresh()
    curses.napms(1500)  # wait 1.5 seconds so user can read it
    stdscr.clear()
    stdscr.refresh()
    curses.curs_set(1)  # show cursor
    word = ""
    suggestion = ""
    sentence = ""
    history = []
    while True:
        key = stdscr.getch()  # waits for 1 keystroke and returns int

        if key == 27:
            quit()

        if key == ord(' '): #space
            history.append(word)
            word = ""
            predictions = ngram.predict(history, 1)
            suggestion = predictions[0] if predictions else ""
            sentence += history[-1] + " "

        elif 32 < key <= 126: #letter
            word += chr(key)
            completions = trie.complete(word, 1)
            suggestion = completions[0] if completions else ""

        elif key == 9:  # Tab
            history.append(suggestion)
            sentence += suggestion + " "
            word = ""
            predictions = ngram.predict(history, 1)
            suggestion = predictions[0] if predictions else ""

        draw(stdscr, word, suggestion, sentence)

def menu(stdscr):
    options = ["Moby Dick", "iMessages", "Reddit"]
    selected = [False, False, False]
    cursor = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select training data (arrow keys to move, space to toggle, enter to confirm):")

        for i, option in enumerate(options):
            checkbox = "[x]" if selected[i] else "[ ]"
            if i == cursor:
                stdscr.addstr(i + 2, 2, f"{checkbox} {option}", curses.color_pair(1))
            else:
                stdscr.addstr(i + 2, 2, f"{checkbox} {option}")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(len(options) - 1, cursor + 1)
        elif key == ord(' '):
            selected[cursor] = not selected[cursor]
        elif key == ord('\n'):
            if any(selected):  # at least one must be selected
                return selected
            else:
                stdscr.addstr(6, 2, "Select at least one!", curses.A_BOLD)
                stdscr.refresh()


def draw(stdscr, word, suggestion, sentence):
    stdscr.clear()
    try:
        max_y, max_x = stdscr.getmaxyx()
        total = sentence + word
        row = len(sentence) // max_x
        col = len(sentence) % max_x

        stdscr.addstr(0, 0, sentence)
        stdscr.addstr(row, col, word)
        stdscr.addstr(row, col + len(word), suggestion[len(word):], curses.A_DIM)
    except curses.error:
        pass
    stdscr.refresh()

curses.wrapper(main)  #setup and cleanup automatic w this