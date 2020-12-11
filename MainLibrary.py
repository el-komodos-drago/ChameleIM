from Cryptography import encrypt, decrypt, GenerateKeypair, Hash, RandomPrime, Num2Text #Num2Text included only for testing
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
    PublicKeyID, salt = RegisterPublicKey()
    PrivateKeyID = SavePrivateKey(PrivateKey)
    SaveKeypair(PublicKeyID, ContactID, PublicKey, Max, PrivateKeyID,salt)
    yield(PublicKeyID,PublicKey,Max)

def CreateInvite(ContactName,filename,destination):
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read()
    IDpassword = Hash(WFK)[1] #This gets a random salt
    ContactID = AddContact(1,1,1,IDpassword,ContactName) # 1s represent blanks
    # these are filled in when a message is recieved
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

def AcceptInvite(ContactName,InputFile,OutputFile):
    contents = lsb.reveal(InputFile)
    try: # check that the data rertived from the file is valid
        print(contents)
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
    ContactID = AddContact(PublicKeyID,PublicKey,Max,IDpassword,ContactName)
    for RerturnedData in CreateKeypair(ContactID): # Create Keypair to send
        if type(RerturnedData) is str:
            yield(RerturnedData)
        else:
            MyPublicKeyID,MyPublicKey,MyMax = RerturnedData
    MessageContents = json.dumps(["Invite Accepted",MyPublicKeyID,MyPublicKey,MyMax])
    SendMessage(OutputFile,MessageContents,IDpassword,PublicKey,Max,ContactID,PublicKeyID)

def WrapMessage(FileName,message,IDpassword,PublicKey,Max):
    #This function stores a message in a image
    message = str(Hash(message,IDpassword)) + message # Prepend HMAC to message
    EncryptedMessage = encrypt(int(PublicKey),int(Max),message) # Encrypt the message
    EncryptedMessage = json.dumps(EncryptedMessage) # Turn to string for stegano
    image = lsb.hide(FileName, EncryptedMessage)
    return(image)

def SendMessage(FileName,message,IDpassword,PublicKey,Max,ContactID,PublicKeyID):
    #This function sends a message to a contact
    #Save the message locally
    MyPublicKeyID, MyPublicKey, MyMax = CurrentSaveDetails(ContactID)
    MessageID = IndexMessage(ContactID, MyPublicKeyID, 1)
    image = WrapMessage(FileName,message,IDpassword,MyPublicKey,MyMax)
    image.save("Messages/"+str(MessageID)+".png")
    
    #Send the message
    image = WrapMessage(FileName,message,IDpassword,PublicKey,Max)
    SendImage(image,MessageID,PublicKeyID)

def GetMessageText(MessageID, PrivateKeyID,Max):
    contents = lsb.reveal("Messages/"+str(MessageID)+".png") 
    CipherText = json.loads(contents)
    with open("PrivateKeys/"+str(PrivateKeyID), "r") as PrivateKeyFile: # DEV NOTE: change once at rest encryption implemented
        PrivateKey = PrivateKeyFile.read()
    MessageText = decrypt(int(PrivateKey),int(Max),CipherText)
    #MessageText = Num2Text([40, 39, 206, 8482, 73, 8211, 104, 108, 92, 120, 49, 48, 92, 120, 56, 49, 176, 92, 120, 49, 51, 120, 179, 8220, 214, 230, 92, 120, 48, 51, 353, 125, 174, 92, 120, 49, 56, 376, 180, 92, 120, 48, 53, 92, 120, 48, 54, 103, 50, 338, 188, 230, 67, 90, 92, 120, 49, 56, 381, 66, 40, 249, 73, 104, 234, 60, 46, 121, 34, 34, 180, 79, 86, 58, 110, 254, 230, 170, 32, 92, 120, 55, 102, 213, 214, 77, 92, 120, 55, 102, 76, 217, 71, 192, 8224, 206, 39, 44, 32, 39, 92, 120, 56, 102, 99, 92, 120, 48, 54, 41, 8221, 92, 120, 48, 101, 92, 120, 57, 100, 119, 97, 92, 120, 56, 49, 48, 201, 218, 119, 170, 92, 110, 87, 236, 52, 220, 229, 108, 382, 121, 8224, 44, 92, 120, 56, 100, 92, 120, 49, 50, 98, 239, 172, 235, 39, 41, 91, 34, 73, 110, 118, 105, 116, 101, 32, 65, 99, 99, 101, 112, 116, 101, 100, 34, 44, 32, 49, 54, 44, 32, 54, 53, 53, 51, 55, 44, 32, 49, 56, 50, 54, 50, 51, 53, 50, 56, 54, 54, 56, 56, 51, 52, 50, 49, 53, 51, 49, 50, 49, 54, 57, 54, 51, 54, 53, 48, 57, 57, 56, 51, 54, 53, 54, 50, 51, 56, 48, 56, 51, 51, 51, 51, 53, 50, 54, 56, 51, 48, 51, 57, 50, 52, 50, 51, 50, 54, 50, 50, 51, 57, 51, 57, 49, 53, 50, 52, 51, 50, 53, 57, 53, 49, 56, 57, 48, 56, 48, 48, 53, 48, 55, 57, 55, 49, 56, 54, 55, 55, 57, 49, 52, 56, 54, 56, 56, 51, 50, 53, 56, 56, 54, 55, 48, 53, 51, 57, 49, 48, 48, 54, 48, 54, 53, 56, 52, 54, 49, 55, 54, 48, 52, 53, 48, 52, 56, 48, 54, 55, 57, 57, 53, 52, 52, 57, 55, 57, 49, 54, 49, 51, 49, 53, 57, 56, 52, 54, 50, 52, 56, 48, 53, 53, 50, 53, 54, 54, 55, 50, 57, 48, 55, 55, 57, 53, 56, 56, 54, 57, 51, 52, 57, 50, 49, 56, 54, 51, 50, 57, 56, 54, 54, 54, 52, 55, 53, 54, 54, 57, 53, 48, 54, 49, 55, 50, 57, 52, 51, 57, 51, 56, 52, 51, 52, 53, 54, 50, 57, 50, 56, 48, 48, 51, 57, 53, 57, 51, 51, 54, 53, 56, 57, 50, 49, 49, 49, 50, 53, 50, 49, 54, 55, 52, 51, 51, 55, 55, 50, 52, 55, 53, 53, 55, 55, 57, 48, 48, 53, 52, 49, 55, 57, 56, 49, 48, 49, 57, 57, 49, 51, 52, 49, 50, 57, 53, 57, 50, 51, 57, 56, 57, 51, 56, 52, 56, 50, 48, 57, 49, 56, 56, 53, 51, 51, 53, 53, 54, 49, 56, 57, 56, 54, 55, 55, 57, 48, 49, 51, 56, 49, 54, 49, 51, 54, 49, 50, 52, 57, 50, 56, 51, 52, 53, 51, 49, 54, 56, 49, 52, 56, 56, 51, 52, 53, 49, 50, 51, 52, 56, 54, 54, 54, 51, 51, 57, 51, 51, 51, 52, 52, 53, 55, 48, 57, 50, 53, 51, 49, 53, 55, 54, 54, 52, 51, 57, 51, 51, 57, 52, 53, 56, 57, 48, 51, 55, 51, 57, 55, 49, 48, 57, 54, 51, 50, 48, 57, 53, 57, 55, 48, 55, 53, 52, 55, 52, 50, 57, 53, 50, 55, 56, 53, 48, 49, 54, 55, 53, 53, 54, 55, 48, 54, 55, 52, 55, 57, 54, 55, 52, 50, 55, 51, 52, 56, 56, 54, 48, 48, 56, 55, 48, 54, 50, 50, 54, 57, 51, 48, 57, 51, 53, 57, 56, 53, 49, 52, 49, 56, 55, 48, 54, 52, 53, 49, 57, 57, 50, 55, 51, 48, 55, 49, 48, 49, 57, 54, 56, 49, 51, 53, 54, 51, 49, 49, 53, 52, 56, 55, 51, 55, 53, 49, 51, 56, 53, 48, 52, 51, 53, 57, 50, 54, 51, 53, 52, 56, 54, 54, 54, 53, 52, 56, 55, 55, 56, 57, 49, 50, 53, 54, 50, 48, 48, 50, 53, 49, 57, 50, 50, 53, 54, 57, 48, 48, 50, 51, 49, 56, 51, 53, 57, 57, 55, 55, 57, 54, 57, 50, 49, 48, 51, 53, 57, 49, 52, 56, 56, 49, 53, 54, 55, 52, 54, 51, 49, 54, 55, 50, 56, 50, 52, 53, 54, 56, 50, 57, 51, 52, 53, 52, 48, 55, 52, 53, 48, 56, 55, 54, 55, 49, 48, 55, 57, 54, 51, 56, 57, 48, 51, 48, 54, 52, 57, 55, 53, 49, 53, 48, 54, 55, 55, 56, 55, 57, 53, 56, 52, 53, 52, 57, 49, 48, 51, 53, 54, 50, 54, 49, 48, 48, 48, 49, 48, 51, 55, 93])
    MessageText = MessageText.split("')")
    Hash = MessageText.pop(0)
    MessageText = "')".join(MessageText)
    print(MessageText)
    Message = json.loads(MessageText)
    return(Message[0])

def PollMessages(ContactID):
    PublicKeyID,PrivateKeyID,Max,salt = CurrentGetDetails(ContactID)
    IDpassword = GetIDpassword(ContactID)
    MesageTexts = [0]
    
    with open("PrivateKeys/"+str(PrivateKeyID), "r") as PrivateKeyFile: 
        PrivateKey = PrivateKeyFile.read()
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read()
        KHash = Hash(WFK,salt)[0]
    
    FileNames = json.loads(GetImageList(PublicKeyID,KHash)) #Dev Note: VALIDATION!!!
    return(FileNames)
    
def OpenMessage(FileName)
    MessageID = IndexMessage(ContactID, PublicKeyID, 0)
    with open("Messages/"+str(MessageID)+".png","wb") as file:
        file.write(GetImage(FileName,PublicKeyID,KHash)) #As above
    DeleteImage(FileName,PublicKeyID,KHash)
    
    contents = lsb.reveal("Messages/"+str(MessageID)+".png")
    CipherText = json.loads(contents)
    MessageText = decrypt(int(PrivateKey),int(Max),CipherText)
    MessageText = MessageText.split("')")
    MessageHash = MessageText.pop(0)+"')"
    MessageText = "')".join(MessageText)
    if MessageHash != str(Hash(MessageText,IDpassword)):
        return()
    
    Message = json.loads(MessageText)
    print(len(Message))
    print("PM 2")
    if len(Message) > 1:
        print("PM - 1")
        MessageContents, ContactPublicKeyID, ContactPublicKey, ContactMax = Message
        UpdateContactKey(ContactID,ContactPublicKeyID, ContactPublicKey, ContactMax)
    return(Message[0])
        


# for attempt in AcceptInvite("Contact 12","C:/Users/zsbel/SparkleShare/ChameleIM/FJR.png"):
#     print(attempt)
# print("ML 1")

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