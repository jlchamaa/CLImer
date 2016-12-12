from resources import session
import curses
Sesh = session.session() 
curses.wrapper(Sesh.play)
