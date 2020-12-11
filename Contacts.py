import sqlite3
import time

def AddContact(PublicKeyID,PublicKey,Max,IDpassword,ContactName):
    with sqlite3.connect("file:data.db?mode=rw", uri=True) as database:
        for row in database.execute("SELECT MAX(ContactID) FROM contacts"):
            ContactID = row[0]+1
        query = """INSERT INTO contacts(ContactID, PublicKeyID, PublicKey, Max, IDpassword,
                   ContactName) VALUES (?,?,?,?,?,?)"""
        data = [ContactID,PublicKeyID,str(PublicKey),str(Max),IDpassword,ContactName]
        database.execute(query, data)
    return(ContactID)

def UpdateContactKey(ContactID, PublicKeyID, PublicKey, Max):
    with sqlite3.connect("file:data.db?mode=rw", uri=True) as database:
        query = """UPDATE contacts SET PublicKeyID=(?), PublicKey=(?), Max=(?)
                    WHERE ContactID = (?)"""
        print([PublicKeyID, PublicKey, Max, ContactID])
        database.execute(query,[PublicKeyID, PublicKey, str(Max), ContactID])
    return()

def SavePrivateKey(PrivateKey):    
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database: #open the database
        for row in database.execute("SELECT MAX(PrivateKeyID) FROM keys"):
            PrivateKeyID = row[0]+1    
    with open("PrivateKeys/"+str(PrivateKeyID), "w") as PrivateKeyFile: #open a file
        PrivateKeyFile.write(str(PrivateKey)) #and save the private key into it
    return(PrivateKeyID)

def SaveKeypair(PublicKeyID, ContactID, PublicKey, Max, PrivateKeyID,salt):
    data = [PublicKeyID,ContactID,1,str(PublicKey),str(Max),PrivateKeyID,salt]
    with sqlite3.connect("file:data.db?mode=rw", uri=True) as database:
        query = """INSERT INTO keys(PublicKeyID, KContactID, Current, PublicKey, Max,
                   PrivateKeyID, salt) VALUES (?,?,?,?,?,?,?)"""
        database.execute(query, data)
    return()
        
def CurrentSaveDetails(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT PublicKeyID, PublicKey, Max FROM keys
                   WHERE KContactID = (?) AND Current = 1"""
        for row in database.execute(query, [str(ContactID)]):
            PublicKeyID,PublicKey,Max = row
    return(PublicKeyID,PublicKey,Max)

def CurrentGetDetails(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT PublicKeyID, PrivateKeyID, Max, salt FROM keys
                   WHERE KContactID = (?) AND Current = 1"""
        for row in database.execute(query, [ContactID]):
            PublicKeyID,PrivateKeyID,Max,salt = row
    return(PublicKeyID,PrivateKeyID,Max,salt)

def RetriveContactIDs():
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        contacts = database.execute("SELECT ContactID FROM contacts WHERE ContactID > 1")
    return(contacts)

def RetriveContacts():
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT DISTINCT contacts.ContactName, contacts.ContactID
                   FROM messages INER JOIN contacts ON 
                   MContactID = contacts.ContactID
                   WHERE contacts.ContactID > 1
                   ORDER BY time"""
        contacts = database.execute(query)
    return(contacts)

def GetContactName(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT ContactName FROM contacts WHERE ContactID = (?)"""
        for row in database.execute(query, [str(ContactID)]):
            ContactName = row[0]
    return(ContactName)

def GetIDpassword(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT IDpassword FROM contacts WHERE ContactID = (?)"""
        for row in database.execute(query, [str(ContactID)]):
            IDpassword = row[0]
    return(IDpassword)

def GetContactKey(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT PublicKeyID, PublicKey, Max, IDpassword
                   FROM contacts WHERE ContactID = (?)"""
        for row in database.execute(query, [str(ContactID)]):
            PublicKeyID,PublicKey,Max,IDpassword = row
    return(PublicKeyID,PublicKey,Max,IDpassword)

def LatestMessageMine(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT Mine FROM messages WHERE MContactID = (?)
                   ORDER BY Time DESC LIMIT 1"""
        for row in database.execute(query, [str(ContactID)]):
            Mine = row[0]
    return(Mine)

def IndexMessage(ContactID, PublicKeyID, mine):
    TimeSent = int(time.time())
    querry = """INSERT INTO messages(MessageID, MContactID, MPublicKeyID, Time, Mine)
                VALUES (?,?,?,?,?)"""
    with sqlite3.connect("file:data.db?mode=rw", uri=True) as database:
        for row in database.execute("SELECT MAX(MessageID) FROM messages"):
            MessageID = row[0]+1
        database.execute(querry,[MessageID,ContactID,PublicKeyID,TimeSent,mine])
    return(MessageID)

def RetriveMessages(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT Mine, MessageID, keys.Max, keys.PrivateKeyID
                   FROM messages INER JOIN keys ON 
                   MPublicKeyID = keys.PublicKeyID
                   WHERE MContactID = (?)
                   ORDER BY time"""
        messages = database.execute(query,[ContactID])
    return(messages)

def RetriveRecentMessages():
    # Gets the MessageID, PrivateKeyID, Max, and ContactID for the 10 most recent messages
    query = """SELECT MessageID, PrivateKeyID, Max, MContactID
               FROM messages INER JOIN keys ON MPublicKeyID = PublicKeyID
               WHERE Mine != 1     -- from other users, not messages sent by this user
               ORDER BY time DESC  -- newest messages (with higher Unix times) first
               LIMIT 10            -- only the first 10"""
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        messages = database.execute(query)
    MessagesList = []
    for message in messages:
        MessagesList.append([message[0],message[1],message[2],GetContactName(message[3]),message[3]])
    return(MessagesList)

with sqlite3.connect("data.db") as database: 
    try: #check tables exist
        ContactIDs = database.execute("SELECT ContactID FROM contacts WHERE ContactID=1")
        for row in ContactIDs:
            print(row)
    except sqlite3.OperationalError: #if it doesn't, create it
        database.execute("""CREATE TABLE contacts (
                        ContactID     integer primary key,
                        PublicKeyID   integer,
                        PublicKey     text,       --must be text, number to big to be integer
                        Max           text,       --must be text, number to big to be integer
                        IDpassword    text,
                        ContactName   text)""")
        query = "INSERT INTO contacts VALUES (?,?,?,?,?,?)"
        database.execute(query, [1,1,1,1,"",""])
        
        database.execute("""CREATE TABLE keys (
                        PublicKeyID  integer primary key,
                        KContactID   integer,
                        Current      integer,
                        PublicKey    text,       --must be text, number to big to be integer
                        Max          text,       --must be text, number to big to be integer
                        PrivateKeyID integer,
                        salt         text,
                        FOREIGN KEY(KContactID) REFERENCES contacts(ContactID))""")
        query = "INSERT INTO keys VALUES (?,?,?,?,?,?,?)"
        database.execute(query, [1,1,1,1,1,1,""])
        
        database.execute("""CREATE TABLE messages (
                        MessageID    integer primary key,
                        MContactID   integer,
                        MPublicKeyID integer,
                        Time         integer,
                        Mine         integer,
                        FOREIGN KEY(MContactID) REFERENCES contacts(ContactID),
                        FOREIGN KEY(MPublicKeyID) REFERENCES keys(PublicKeyID))""")
        query = "INSERT INTO messages VALUES (?,?,?,?,?)"
        database.execute(query, [1,1,1,1,1])

