import sqlite3
import os
class dbO:
    def __init__(self):
        self.connectToDataBase()

    def connectToDataBase(self):
        requiredDbPath = self.getResourcePath()
        if(os.path.isfile(requiredDbPath)):
            self.db = sqlite3.connect(requiredDbPath)
        else:
            self.db = self.createDb(requiredDbPath)

    def getResourcePath(self):
        pathOfResources = os.path.dirname(os.path.abspath(__file__))
        requiredDbPath = pathOfResources + "/times.db"
        return requiredDbPath

    def createDb(self,requiredDbPath):
        db = sqlite3.connect(requiredDbPath)
        db.execute("""CREATE TABLE TIMES
                    (session text, time real, plusTwo int, date text, scramble text)""")
        return db

    def deliverDb(self,seshName):
        retObj = []
        sessionName = (seshName,)
        dbCurs = self.db.execute("""    SELECT time , plusTwo FROM TIMES  
                                            WHERE session=?;""",sessionName)
        for record in dbCurs: 
            retObj.append(record)
        return retObj

    def getAllSessionNames(self):
        allSessionNames = []
        dbCurs = self.db.execute("""    SELECT DISTINCT session FROM TIMES
        """)
        for record in dbCurs:
            allSessionNames.append(str(record[0]))
        return allSessionNames

    def writeDb(self,solve):
        self.db.execute("INSERT INTO TIMES VALUES (?,?,?,?,?)",(solve['session'],solve['time'],solve['plusTwo'],solve['date'],solve['scramble']))
        self.db.commit()
