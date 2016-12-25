from resources import session
import curses
def main(stdscr):
    sesh = session.session(stdscr)
    sesh.play()
curses.wrapper(main)
print "Thanks for playing!"
