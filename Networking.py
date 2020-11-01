from Cryptography import Hash
import sqlite3

def RegisterPublicKey():
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read() #Save the contents of the WiFall Key file to WFK
    KHash,salt = Hash(WFK) #get the hash and salt by Hashing it
    
    #Replace this with sever connection
    with sqlite3.connect("file:data.db?mode=ro", uri=True) as database: #open the database
        for row in database.execute("SELECT MAX(PublicKeyID) FROM keys"):
            #Find the largest PublicKeyID and save a value 1 higher to a variable
            PublicKeyID = row[0]+1
    print()
    return(PublicKeyID,salt)

def SendImage(image,MessageID,PublicKeyID):
    image.save("ToServer/"+str(MessageID)+".png")
    print("Done")