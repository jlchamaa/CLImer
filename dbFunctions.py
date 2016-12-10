import sqlite3
import os
def createDb():
    db = sqlite3.connect("times.db")
    db.execute('''CREATE TABLE TIMES
		 (session text, time real, plusTwo int, date text, scramble text)''')
    return c
def connectDb():
    if(os.path.isfile("./times.db")):
        return sqlite3.connect("times.db")
    else:
        return createDatabase()

def printDb(db):
    for record in db.execute("SELECT * FROM TIMES"):
        print record

def writeDb(db,session,time,plusTwo,date,scramble):
    db.execute("INSERT INTO TIMES VALUES (?,?,?,?,?)",(session,time,plusTwo,date,scramble))
