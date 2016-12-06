import time
import curses

def initializeWindows(stdscr):
    windowArray= []
    windowArray.append(stdscr)
    for i in range(1,5): #inconsequential iterator
        windowArray.append(curses.newwin(1,1,0,0))
    return windowArray

#   stdscr = 0
#  ############
#  # 1    # 2 #
#  #      #   #
#  ############
#  #  3   # 4 #
#  ############

def resizeWindows(windowArray):
    (maxY,maxX) = windowArray[0].getmaxyx()
    horizontalDividerIndex = int(round(maxY*0.8))
    verticalDividerIndex = int(round(maxX*0.8))
    windowArray[1].resize(horizontalDividerIndex-1,verticalDividerIndex-1)
    windowArray[2].mvwin(0,verticalDividerIndex+1)
    windowArray[2].resize(horizontalDividerIndex-1,maxX-verticalDividerIndex+1)
    windowArray[3].mvwin(horizontalDividerIndex+1,0)
    windowArray[3].resize(maxY-horizontalDividerIndex+1,verticalDividerIndex-1)
    windowArray[4].mvwin(horizontalDividerIndex+1,verticalDividerIndex+1)
    windowArray[4].resize(maxY-horizontalDividerIndex+1,maxX-verticalDividerIndex+1)

def refreshWindows(windowArray):
    for i in range(1,5):
        windowArray[i].border()
        windowArray[i].addstr(1,1,str(i))
        windowArray[i].refresh()
        tempChar = windowArray[i].getch()
        windowArray[i].addch(tempChar)
        windowArray[i].refresh()

#def processMainInput(inputKey,windowArray):

def timer(stdscr):
    d="p"; # not space
    curtime=0
    stdscr.addstr(15,0, "Timer running")
    start = time.time()
    stdscr.nodelay(1)
    while(d!=32): #character for space
        now = time.time()
        tick = round(now-start,2); 
        if(curtime!=tick):
            curtime=tick;
            stdscr.addstr(17,0, str(curtime))
        d=stdscr.getch()

def main(stdscr):
    windowArray = initializeWindows(stdscr)
    resizeWindows(windowArray)
    refreshWindows(windowArray)
    mainInput = windowArray[1].getkey() # wait for ch input from user
    processMainInput(mainInput,windowArray)
curses.wrapper(main)
