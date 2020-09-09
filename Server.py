from Cryptography import Hash

def RegisterPublicKey(PublicKey):
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read() #Save the contents of the WiFall Key file to WFK
    Hash,salt = Hash(WFK) #get the hash and salt from Hashing it
    
    #Replace this with sever connection
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database: #open the database
        for row in database.execute("SELECT MAX(PublicKeyID) FROM keys"):
            #Find the largest PublicKeyID and save a value 1 higher to a variable
            PublicKeyID = row[0]+1
    return(salt,PublicKeyID)