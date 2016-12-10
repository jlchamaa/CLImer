import dbFunctions

x = dbFunctions.connectDb()
dbFunctions.writeDb(x,"chamaa",20.45,1,"12-4-8","R' U D' L")
dbFunctions.printDb(x)
