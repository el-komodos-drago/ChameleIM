import sqlite3
from os import path

def RetriveMessages(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT MessageID, Mine, keys.PrivateKeyID
                   FROM messages INER JOIN keys ON 
                   PublicKeyID = keys.PublicKeyID
                   WHERE MContactID = (?)
                   ORDER BY time"""
        messages = database.execute(query,str(ContactID))
    for message in messages:
        print(message)
    #DEV NOTE INSERT CODE HERE

def AddContact(PublicKey,Max,IDpassword,ContactName):
    with sqlite3.connect("data.db") as database: #open the database
        for row in database.execute("SELECT MAX(ContactID) FROM contacts"):
            ContactID = row[0]+1
        query = "INSERT INTO messages VALUES (?,?,?,?,?)"
        data.execute(query, [ContactID,PublicKey,Max,IDpassword,ContactName])
    return(ContactID)
        


def GetKeyIDs(PrivateKey):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database: #open the database
        for row in database.execute("SELECT MAX(PublicKeyID) FROM keys"):
            #Find the largest PublicKeyID and save a value 1 higher to a variable
            PublicKeyID = row[0]+1
        for row in database.execute("SELECT MAX(PrivateKeyID) FROM keys"):
            PrivateKeyID = row[0]+1
    #print("PublicKeyID "+str(PublicKeyID))
    
    with open("PrivateKeys/"+str(PrivateKeyID), "w") as PrivateKeyFile:
        PrivateKeyFile.write(str(PrivateKey))
    return(PublicKeyID,PrivateKeyID)




def SaveKeypair(PublicKeyID, ContactID, PublicKey, Max, PrivateKey):
    with sqlite3.connect("data.db") as database:
        query = "INSERT INTO keys VALUES (?,?,?,?,?)"
        database.execute(query, [PublicKeyID,ContactID,1,PublicKey,Max,PrivateKey])




with sqlite3.connect("data.db") as data: 
    try: #check tables exist
        ContactIDs = data.execute("SELECT ContactID FROM contacts WHERE ContactID=1")
        for row in ContactIDs:
            print(row)
    except sqlite3.OperationalError: #if it doesn't, create it
        data.execute("""CREATE TABLE contacts (
                        ContactID   integer primary key,
                        PublicKey   integer,
                        Max         integer,
                        IDpassword  text,
                        ContactName text)""")
        query = "INSERT INTO contacts VALUES (?,?,?,?,?)"
        data.execute(query, [1,1,1,"",""])
        
        data.execute("""CREATE TABLE keys (
                        PublicKeyID  integer primary key,
                        KContactID   integer,
                        Current      integer,
                        PublicKey    integer,
                        Max          integer,
                        PrivateKeyID integer,
                        salt         
                        FOREIGN KEY(KContactID) REFERENCES contacts(ContactID))""")
        query = "INSERT INTO keys VALUES (?,?,?,?,?)"
        data.execute(query, [1,1,1,1,1])
        
        data.execute("""CREATE TABLE messages (
                        MessageID    integer primary key,
                        MContactID   integer,
                        MPublicKeyID integer,
                        Time         integer,
                        Mine         integer,
                        FOREIGN KEY(MContactID) REFERENCES contacts(ContactID),
                        FOREIGN KEY(MPublicKeyID) REFERENCES keys(PublicKeyID))""")
        query = "INSERT INTO messages VALUES (?,?,?,?,?)"
        data.execute(query, [1,1,1,1,1])

RetriveMessages(1)