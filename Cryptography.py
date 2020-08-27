#This is an area to test code.
print("This code was not created by a cryptographic expert and has not been reviewed.")
print("Under no circumstances should it be used for real world perposes")

from math import sqrt
from os import urandom
import time
from Cryptodome.Util import number
from hashlib import pbkdf2_hmac as HashFunction
from secrets import SystemRandom

def Num2Text (numbers):
    text = ""
    for number in numbers:
        character = chr(number)
        text = text + character
    return(text)



###############################
#####  START OF RSA CODE  #####
###############################
def RandomPrime(bits,prime = 0): #this function returns a random prime that is larger than 258
    while prime < 258: # While prime isn't large enough for RSA...
        prime = number.getPrime(bits) # Change prime to random value created through getPrime
    return(prime) # Return that prime

#Coded using https://gist.github.com/JonCooperWorks/5314103 as a reference

def GreatestCommonDivisor (number1, number2): # Euclid's algorithm
    #This code finds the greatest common divisor of two numbers.
    #this means the largest number both can be divided by with the result being a whole number
        
    if number2 > number1: #if number2 is bigger than number 1...
        number2, number1 = number1, number2 #flip number1 and number2 over
    
    remainder = number1 % number2
    if remainder == 0: # if number 2 already divides number 1 perfectly...
        return(number2) #then it is the greatest common divisor
    # We only need to find the GCD of number 2 and the remainder as if it divides number 2,
    # it will also divide the part of the number that isn't the remainder.
    # See https://medium.com/i-math/why-does-the-euclidean-algorithm-work-aaf43bd3288e
    return(GreatestCommonDivisor(number2, remainder))

def MultiplicitveInverse(PublicKey, phi): #Euclid's Extended Algorithm
    #This finds the Modular Multiplicitve Inverse.
    # A regular inverse is 1 divided by a number, let's call the original number a.
    # A multiplicitive inverse of a number which when multiplied with a equals 1.
    # Normally a multiplicitive inverse is the same as a regular inverse.
    # But a modular multiplicitive inverse is a multiplicitive inverse of a number
    # in a finite field.
    
    # As a result this finds a value of d such that PublicKey * PrivateKey = 1
    # in the finite field defined by phi
    # (ie a value of d where (PublicKey * PrivateKey)/phi leaves a remainder of 1)
    
    #Built using https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    #as a reference implimentation.
    
    #Initialise assorted variables
    OldRemainder = PublicKey
    remainder = phi
    S = 0
    OldS = 1
    
    while remainder != 0:
        temp = remainder #temporarily save the remainder...
        quotient, remainder = divmod(OldRemainder, remainder) #...do stuff...
        OldRemainder = temp #... then transfer the previous remainder into OldRemainder
        
        temp = S #temporarily save S ...
        S = OldS - (quotient * S) #...do stuff...
        OldS = temp #... then transfer the pervious S into OldS
        
    return(OldS)

def GenerateKeypair (p, q):
    Max = p * q
    phi = (p-1) * (q-1) #phi is the totient of Max
    
    # Pick e
    if phi <= 65537:
        return("PickLargerPrimes")
    PublicKey = 65537 #might seem weird but this is what 95.5% of CAs do.
    # https://www.johndcook.com/blog/2018/12/12/rsa-exponent/
    GCD = GreatestCommonDivisor(PublicKey,phi)
    while GCD != 1:
        PublicKey = SystemRandom.randrange(1000,phi)
        GCD = GreatestCommonDivisor(PublicKey,phi)
    
    #calculate the PublicKey
    PrivateKey = MultiplicitveInverse(PublicKey, phi)
    
    return(Max, PublicKey, PrivateKey)

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
    length = len(ciphertext)
    ciphertext = ciphertext.encode("ANSI")
    for i in range(0,length,256):
        print()
    
    
    
    plaintext = []
    for character in ciphertext: #breaks up the ciphertext into a series of characters and opperates on each of them indiidually.
        PlainChar = pow(character, PrivateKey, Max)
        # Multiply the numeric representation of the character by itself the number of times
        # specified by the public key, then subtract Max from it until the number left is
        # less than Max.
        plaintext.append(PlainChar) # Attach the encrypted character to the end of the plaintext
    return (plaintext)

#############################
#####  END OF RSA CODE  #####
#############################

def Hash(data, salt = urandom(32)): #hash string with a salt that defaults to 16 urandom bytes
    if type(salt) == str:
        salt = salt.encode("ANSI")
    HashResult = HashFunction("sha512",data.encode("utf-8"),salt,100000)
    return(HashResult.decode("ANSI"),salt.decode("ANSI"))

length = 1024
for i in range(0,length,256):
    print(i)

#PublicKey = 3964486370077782136612550498210702476142931137799038117416017536242213248482719936071208387244876798784689284468145050928140716887800785525799179677842781831645962121128175613561683054780427898162005724797133575660572518222854167891121786702375394572058203720113113550349024245975916542957999141837568973893665560117236205814582359361410901868765125994020517687497225371004137626719299852743104173002213194923676990423262849315382393723144152835517039263563053406454530411077498624393593810025444354767899268362774725150823727653283577625524824702881456667051106520786019171274998511003613147088979254072221089426265
#Max = 16573358629571193971243013459286522177647463033612015124136859174121702472782548730643540478080467612550371986744199923625537932172979529310729147065559889832275398324448379484977484363152701611395252228489490536969250566228946456661379634822579334953688747668881362680948140716241860207682489619098600359894954159129702083274478514578418831613696632617373401164302622662629377562382861959123944984517715648054901233757656305001971188784365862673036427416948526827545178262935463301685499801363406211259999046596385768633191852353302026332821911382341024938942264819065929079996055763405469415032161199606380406058911
#print(encrypt(PublicKey,Max,"Some Text"))