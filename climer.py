from resources import session
import curses
def main(stdscr):
    sesh = session.session(stdscr)
    sesh.play()
try:
    curses.wrapper(main)
    print("Thanks for playing!")
except ValueError as ex:
    if str(ex) == 'toosmall':
        print("Window too narrow.  Try resizing!")
    else:
        raise
