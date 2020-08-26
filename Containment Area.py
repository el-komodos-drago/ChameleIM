from Cryptography import *
from Contacts import *

def CreateKeypair(ContactID):
    PrivateKey = -1
    while PrivateKey < 0:
        prime1,prime2 = RandomPrime(1024),RandomPrime(1024) #create 2 random primes
        Max, PublicKey, PrivateKey = GenerateKeypair(prime1, prime2)
    
    PublicKeyID, PrivateKeyID = GetKeyIDs(PrivateKey)
    SaveKeypair(PublicKeyID, ContactID, PublicKey, Max, PrivateKeyID)

def CreateInvite():
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read()
        print(Hash(WFK))
        input()
        
CreateInvite()

CreateKeypair(ContactID)

# print(Max, PublicKey, PrivateKey)
# 
# text = input()
# cipher = encrypt(PublicKey,Max,text)
# 
# plain = decrypt(PrivateKey,Max,cipher)
# print(plain)
# print(Num2Text(plain))