import sqlite3
import os
class dbO:
    def __init__(self):
        pathOfResources = os.path.dirname(os.path.abspath(__file__))
        requiredDbPath = pathOfResources + "/times.db"
        if(os.path.isfile(requiredDbPath)):
            self.db = sqlite3.connect(requiredDbPath)
        else:
            self.db = self.createDb(requiredDbPath)

    def createDb(self,requiredDbPath):
        db = sqlite3.connect(requiredDbPath)
        db.execute('''CREATE TABLE TIMES
                    (session text, time real, plusTwo int, date text, scramble text)''')
        return db
    def printDb(self):
        for record in db.execute("SELECT * FROM TIMES"):
            print record

    def writeDb(self,session,time,plusTwo,date,scramble):
        self.db.execute("INSERT INTO TIMES VALUES (?,?,?,?,?)",(session,time,plusTwo,date,scramble))
