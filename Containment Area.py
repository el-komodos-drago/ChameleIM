from Cryptography import *
from Contacts import *
from stegano import lsb

def CreateKeypair(ContactID):
    PrivateKey = -1
    while PrivateKey < 0:
        prime1,prime2 = RandomPrime(1024),RandomPrime(1024) #create 2 random primes
        Max, PublicKey, PrivateKey = GenerateKeypair(prime1, prime2)
    
    PublicKeyID, PrivateKeyID = GetKeyIDs(PrivateKey)
    SaveKeypair(PublicKeyID, ContactID, PublicKey, Max, PrivateKeyID)
    return(PublicKey,Max)

def CreateInvite(ContactName):
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read()
        IDpassword = Hash(WFK)[1] #This gets a random salt
    ContactID = AddContact(1,1,IDpassword,ContactName)
    PublicKey,Max = CreateKeypair(ContactID)

ContactName = input("Please enter contact name: ")

CreateInvite(ContactName)

CreateKeypair(ContactID)

# print(Max, PublicKey, PrivateKey)
# 
# text = input()
# cipher = encrypt(PublicKey,Max,text)
# 
# plain = decrypt(PrivateKey,Max,cipher)
# print(plain)
# print(Num2Text(plain))