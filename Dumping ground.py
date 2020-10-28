print("This file contains sub routines that were created for but not used in the main program")
def RandomPrime(cap,prime=([True] * 100000000)):
    #Sieve of Eratosthenes using
    #https://www.geeksforgeeks.org/python-program-for-sieve-of-eratosthenes/
    #as a reference implimentation
    #returns the largest random prime before the cap
    
    #creates a list of length cap with all values being True.
    print("bg")
#    prime = [True for i in range(cap + 1)] 
#     prime = []
#     for i in range (0,cap+1):
#         prime.append(True)
    
    print("2")
    for itteration in range(2, int(sqrt(cap)+1)):
        if prime[itteration] == True: #if itteration is prime...
            #print(str(itteration))
            for i in range(itteration*2, cap+1, itteration):
                prime[i] = False #mark all multiples of itteration as not prime
    print("as")
    for itteration in range(cap,0,-1):
        if prime[itteration] == True:
            return(itteration)

def CheckPrime (number): # checks if a number is prime
    # Primes are numbers that can not be formed by multiplying two other whole numbers
    # numbers that aren't prime are known as composit numbers and the whole numbers they can
    # be divided by are known as factors.
    if number == 1:
        return(False) # discards 1
    if number % 2 == 0:
        return(False) # excludes even numbers
    if number % 3 == 0:
        return(False) # excludes numbers that are multiples of 3
    limit = sqrt(number) + 2 # set the limit to the square root of the number.
    # If the smallest of the two numbers being multiplied is larger than the square root of
    # the number being tested then the result will be larger than the number being tested.
    # We only need to test the smaller of the potential factors because that will also test
    # the larger factor they pair up with.
    
    for iteration in range(3, int(limit)+1, 2):
        #checks odd numbers between 3 and half the value of the number
        #Dev note, upgrade to check 6i - 1 and 6i + 1
        if number % iteration == 0:
            return(False)
    return(True)



def CreateInvite(ContactName):
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read()
    IDpassword = Hash(WFK)[1] #This gets a random salt
    ContactID = AddContact(1,1,IDpassword,ContactName)
    PublicKeyID,PublicKey,Max = CreateKeypair(ContactID)
    PublicKeyID = PublicKeyID.to_bytes(8,"big")
    PublicKey = PublicKey.to_bytes(256,"big")
    Max = Max.to_bytes(256,"big")
    SecretData = (PublicKeyID+PublicKey+Max).decode("ANSI")
    print(SecretData)
    filename = input("Input file name: ")
    destination = input("Output file name: ")
    file = lsb.hide(filename, SecretData)
    file.save(destination)
    return(SecretData)

def encrypt(PublicKey, Max, plaintext):
    ciphertext = b''
    for character in plaintext: #breaks up plaintext into a series of characters and then for each of them ...
        CharCode = ord(character) #converts the character into it's numeric representation
        CipherChar = pow(CharCode, PublicKey, Max)
        # Multiply the numeric representation of the character by itself the number of times
        # specified by the public key, then subtract Max from it until the number left is
        # less than Max.
        ciphertext = ciphertext + CipherChar.to_bytes(256,"big") # Attach the encrypted character to the end of the ciphertext
    return(ciphertext.decode("ANSI"))

def decrypt(PrivateKey, Max, ciphertext):
    length = len(ciphertext) #get the length of the ciphertext
    ciphertext = ciphertext.encode("ANSI") #convert to binary
    CipherChars = [] # create empty list
    for i in range(0,length,256): # for every multiple of 256 up to the ciphertext's length ...
        Binary = ciphertext[i:i+256] # ... take bytes from that multiple to the next ...
        CipherChar = int.from_bytes(Binary,byteorder="big") # ... convert them to an integer...
        CipherChars.append(CipherChar) # ... and append the integer to CipherChars
    
    plaintext = []
    for character in CipherChars: #breaks up the ciphertext into a series of characters and opperates on each of them indiidually.
        PlainChar = pow(character, PrivateKey, Max)
        # Multiply the numeric representation of the character by itself the number of times
        # specified by the public key, then subtract Max from it until the number left is
        # less than Max.
        plaintext.append(PlainChar) # Attach the encrypted character to the end of the plaintext
    return (plaintext)

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