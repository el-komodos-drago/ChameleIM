import sqlite3
import json

def IndexMessage(filename,address):
   with sqlite3.connect("data.db") as database:
      database.execute("INSERT INTO messages(filename,address) VALUES (?,?)",[filename,address])

def RegisterPublicKey(password):
   with sqlite3.connect("data.db") as database:
      for row in database.execute("SELECT MAX(PublicKeyID) FROM PublicKeys"):
         PublicKeyID = row[0]+1
      data = [PublicKeyID, password]
      database.execute("INSERT INTO PublicKeys(PublicKeyID, SaltedWFK) VALUES (?,?)",data)
   return(PublicKeyID)

def CorrectCredentials(PublicKeyID,KHash,filename):
   trace = []
   correct = False
   trace.append(correct)
   with sqlite3.connect("data.db") as database:
      query = "SELECT SaltedWFK FROM PublicKeys WHERE PublicKeyID = (?)"
      for row in database.execute(query,[int(PublicKeyID)]):
         print(row[0])
         print(KHash)
         if row[0] == KHash:
            correct=True
      trace.append(correct)
      print(correct)
      if filename != "None":
         query = "SELECT address FROM messages WHERE filename=(?)"
         for row in database.execute(query,[filename]):
            if str(row[0]) != str(PublicKeyID):
               correct=False
      trace.append(correct)
   return(correct,trace)

def GetMessages(PublicKeyID):
   with sqlite3.connect("data.db") as database:
      query = "SELECT filename FROM messages WHERE address = (?)"
      filenames = []
      for row in database.execute(query,[PublicKeyID]):
         filenames.append(row[0])
   return(json.dumps(filenames))

with sqlite3.connect("data.db") as database:
    try: #check tables exist
        PublicKeyIDs = database.execute("SELECT PublicKeyID FROM PublicKeys WHERE PublicKeyID=1")
        for row in PublicKeyIDs:
            print(row)
    except sqlite3.OperationalError: #if it doesn't, create it
        database.execute("""CREATE TABLE PublicKeys (
                            PublicKeyID integer primary key,
                            SaltedWFK   text)""")
        database.execute("INSERT INTO PublicKeys(PublicKeyID,SaltedWFK) VALUES (?,?)",[1,"a"])
        database.execute("""CREATE TABLE messages (
                            filename text primary key,
                            address integer,
                            FOREIGN KEY(address) REFERENCES PublicKeys(PublicKeyID))""")
        database.execute("INSERT INTO messages(filename, address) VALUES (?,?)",["a",1])