#This is an area to test code.
print("This code was not created by a cryptographic expert and has not been reviewed.")
print("Under no circumstances should it be used for real world perposes")

from math import sqrt
from random import randrange
import random
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
        PublicKey = randint(1000,phi) #Randrange is not cryptographically secure. Doesn't need to be.
        GCD = GreatestCommonDivisor(PublicKey,phi)
    
    #calculate the PublicKey
    PrivateKey = MultiplicitveInverse(PublicKey, phi)
    
    return(Max, PublicKey, PrivateKey)

def encrypt(PublicKey, Max, plaintext):
    ciphertext = []
    for character in plaintext: #breaks up plaintext into a series of characters and then for each of them ...
        CharCode = ord(character) #converts the character into it's numeric representation
        CipherChar = pow(CharCode, PublicKey, Max)
        # Multiply the numeric representation of the character by itself the number of times
        # specified by the public key, then subtract Max from it until the number left is
        # less than Max.
        ciphertext.append(CipherChar) # Attach the encrypted character to the end of the ciphertext
    return(ciphertext)

def decrypt(PrivateKey, Max, ciphertext):
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

def Hash(data, salt = urandom(16)): #hash string with a salt that defaults to 16 urandom bytes
    if isinstance(salt, str):
        salt = salt.encode("ANSI")
    HashResult = HashFunction("sha512",data.encode("utf-8"),salt,100000)
    return(HashResult.decode("ANSI"),salt.decode("ANSI"))

t0 = time.time()
rn = random.randrange(1000,10000000000)
t1 = time.time()
print (t0 - t1)
print(rn)