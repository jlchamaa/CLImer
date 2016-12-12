import sqlite3
import os
class dbO:
    def __init__(self):
        if(os.path.isfile("./times.db")):
            self.db = sqlite3.connect("times.db")
        else:
            self.db = self.createDb()

    def createDb(self):
        db = sqlite3.connect("times.db")
        db.execute('''CREATE TABLE TIMES
                    (session text, time real, plusTwo int, date text, scramble text)''')
        return db
    def printDb(self):
        for record in db.execute("SELECT * FROM TIMES"):
            print record

    def writeDb(self,session,time,plusTwo,date,scramble):
        self.db.execute("INSERT INTO TIMES VALUES (?,?,?,?,?)",(session,time,plusTwo,date,scramble))
