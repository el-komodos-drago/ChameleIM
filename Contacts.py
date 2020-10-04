import sqlite3
import time

def AddContact(PublicKey,Max,IDpassword,ContactName):
    with sqlite3.connect("data.db") as database:
        for row in database.execute("SELECT MAX(ContactID) FROM contacts"):
            ContactID = row[0]+1
        query = """INSERT INTO contacts(ContactID, PublicKey, Max, IDpassword, ContactName)
                   VALUES (?,?,?,?,?)"""
        database.execute(query, [ContactID,str(PublicKey),str(Max),IDpassword,ContactName])
    return(ContactID)

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

def RetriveContacts():
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT DISTINCT contacts.ContactName, contacts.ContactID
                   FROM messages INER JOIN contacts ON 
                   MContactID = contacts.ContactID
                   WHERE contacts.ContactID > 1
                   ORDER BY time"""
        contacts = database.execute(query)
    return(contacts)
            

def IndexMessage(ContactID, PublicKeyID, mine):
    TimeSent = int(time.time())
    querry = """INSERT INTO messages(MessageID, MContactID, MPublicKeyID, Time, Mine)
                VALUES (?,?,?,?,?)"""
    with sqlite3.connect("data.db") as database:
        for row in database.execute("SELECT MAX(MessageID) FROM messages"):
            MessageID = row[0]+1
        database.execute(querry,[MessageID,ContactID,PublicKeyID,TimeSent,mine])
    return(MessageID)

def RetriveMessages(ContactID):
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        query = """SELECT MessageID, Mine, keys.PrivateKeyID
                   FROM messages INER JOIN keys ON 
                   PublicKeyID = keys.PublicKeyID
                   WHERE MContactID = (?)
                   ORDER BY time"""
        messages = database.execute(query,[ContactID])
    for message in messages:
        print(message)
    #DEV NOTE INSERT CODE HERE

def RetriveRecentMessages():
    query = """SELECT MessageID, contacts.ContactName, keys.PrivateKeyID
                   FROM messages INER JOIN keys ON PublicKeyID = keys.PublicKeyID
                   INER JOIN contacts ON MContactID = contacts.ContactID
                   WHERE Mine != 1
                   ORDER BY time DESC
                   LIMIT 10"""
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database:
        messages = database.execute(query)
    return(messages)

with sqlite3.connect("data.db") as data: 
    try: #check tables exist
        ContactIDs = data.execute("SELECT ContactID FROM contacts WHERE ContactID=1")
        for row in ContactIDs:
            print(row)
    except sqlite3.OperationalError: #if it doesn't, create it
        data.execute("""CREATE TABLE contacts (
                        ContactID   integer primary key,
                        PublicKey   text,       --must be text, number to big to be integer
                        Max         text,       --must be text, number to big to be integer
                        IDpassword  text,
                        ContactName text)""")
        query = "INSERT INTO contacts VALUES (?,?,?,?,?)"
        data.execute(query, [1,1,1,"",""])
        
        data.execute("""CREATE TABLE keys (
                        PublicKeyID  integer primary key,
                        KContactID   integer,
                        Current      integer,
                        PublicKey    text,       --must be text, number to big to be integer
                        Max          text,       --must be text, number to big to be integer
                        PrivateKeyID integer,
                        salt         text,
                        FOREIGN KEY(KContactID) REFERENCES contacts(ContactID))""")
        query = "INSERT INTO keys VALUES (?,?,?,?,?,?,?)"
        data.execute(query, [1,1,1,1,1,1,""])
        
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