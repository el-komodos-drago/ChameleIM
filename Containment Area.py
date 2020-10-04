

def Num2String(integer):
    itteration = 256
    string = ""
    while itteration < integer:
        character = chr(integer % itteration)
        string = string + character
        integer = integer // itteration
        itteration = itteration * 256
    string = str(chr(integer)) +string
    return(string)
def String2Num(string):
    integer = ord(string[0])
    for i in range(len(string)-1):
        character = string[i+1]
        CharCode = ord(character)*(256**(i))
        integer =+ CharCode
    return(integer)

def CreateKeypair(ContactID):
    PrivateKey = -1
    print("Generating keypair")
    attempt = 0
    while PrivateKey < 0:
        attempt += 1
        yield(str(attempt))
        prime1,prime2 = RandomPrime(1024),RandomPrime(1024) #create 2 random primes
        Max, PublicKey, PrivateKey = GenerateKeypair(prime1, prime2)
    print("Finished generation")
    PublicKeyID, salt = RegisterPublicKey(PublicKey)
    PrivateKeyID = SavePrivateKey(PrivateKey)
    SaveKeypair(PublicKeyID, ContactID, PublicKey, Max, PrivateKeyID,salt)
    return(PublicKeyID,PublicKey,Max)

ContactName = "AVeryLongName"
MaxCharacters = 10
ContactName = ContactName[0:(MaxCharacters-3)]+"..."
print(ContactName)

#string = Num2String(1259)
#print(string)
#print(String2Num(string))