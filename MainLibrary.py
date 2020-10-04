from Cryptography import encrypt, decrypt, GenerateKeypair, Hash, RandomPrime
from Contacts import *
from Networking import *
from stegano import lsb
import json
import time

def CreateKeypair(ContactID):
    PrivateKey = -1
    attempt = 0
    while PrivateKey < 0:
        attempt += 1
        yield("Generating Keypair, Attempt: "+str(attempt))
        prime1,prime2 = RandomPrime(1024),RandomPrime(1024) #create 2 random primes
        Max, PublicKey, PrivateKey = GenerateKeypair(prime1, prime2)
    yield("Finished generation, uploading public key to server")
    PublicKeyID, salt = RegisterPublicKey(PublicKey)
    PrivateKeyID = SavePrivateKey(PrivateKey)
    SaveKeypair(PublicKeyID, ContactID, PublicKey, Max, PrivateKeyID,salt)
    yield(PublicKeyID,PublicKey,Max)

def CreateInvite(ContactName,filename,destination):
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read()
    IDpassword = Hash(WFK)[1] #This gets a random salt
    ContactID = AddContact(1,1,IDpassword,ContactName)
    for RerturnedData in CreateKeypair(ContactID):
        if type(RerturnedData) is str:
            yield(RerturnedData)
        else:
            PublicKeyID,PublicKey,Max = RerturnedData
            yield("Saving invite")
    InviteData = [PublicKeyID,PublicKey,Max,IDpassword] # combined variables into a list
    InviteData = json.dumps(InviteData) # turn InviteData into a string with JSON for Stegano
    file = lsb.hide(filename, InviteData)
    file.save(destination)

def AcceptInvite(ContactName,FileName):
    contents = lsb.reveal(FileName)
    try: # check that the data rertived from the file is valid
        PublicKeyID,PublicKey,Max,IDpassword = json.loads(contents)#take variables out of JSON
        PublicKeyID,PublicKey,Max = int(PublicKeyID),int(PublicKey),int(Max)
        # Convert variables to integers to check they are integers
        if PublicKey > Max:  #ensure PublicKey is smaller than Max
            raise ValueError
        if PublicKeyID > 9223372036854775807: #ensure PublicKeyID is small enough for database
            raise ValueError
        if Max > (2 ** 2048): #ensure max small enough to be real
            raise ValueError
        if PublicKey < 10000:
            raise ValueError
    except (ValueError,json.decoder.JSONDecodeError):
        print("Invalid invite file") #if not JSON: JSONDecodeError; if wrong JSON: ValueError
        return()
    PublicKeyID = None #Blank PublicKeyID as currently unused
    ContactID = AddContact(PublicKey,Max,IDpassword,ContactName)
    for RerturnedData in CreateKeypair(ContactID): # Create Keypair to send
        if type(RerturnedData) is str:
            yield(RerturnedData)
        else:
            MyPublicKeyID,MyPublicKey,MyMax = RerturnedData
    MessageContents = json.dumps(["Invite Accepted",MyPublicKeyID,MyPublicKey,MyMax])
    SendMessage(MessageContents,IDpassword,PublicKey,Max,ContactID, MyPublicKeyID)

def SendMessage(message,IDpassword,PublicKey,Max,ContactID, PublicKeyID):
    MessageID = IndexMessage(ContactID, PublicKeyID, 1)
    message = Hash(message,IDpassword) + message # Prepend HMAC to message
    EncryptedMessage = encrypt(PublicKey,Max,message) # Encrypt the message
    
    EncryptedMessage = json.dumps(EncryptedMessage) # Turn to string for stegano
    FileName = input()
    image = lsb.hide(FileName, EncryptedMessage)
    SendImage(image,MessageID)

#input()

#ContactName = "Aardvark" #input("Please enter contact name: ")

#CreateInvite(ContactName)

#ContactName = "Arnald"
#FileName = "Thing.png"
#AcceptInvite(ContactName,FileName)


# print(Max, PublicKey, PrivateKey)
# 
# text = input()
# cipher = encrypt(PublicKey,Max,text)
# 
# plain = decrypt(PrivateKey,Max,cipher)
# print(plain)
# print(Num2Text(plain))