#This is an area to test code.
print("This code was not created by a cryptographic expert and has not been reviewed.")
print("Under no circumstances should it be used for real world perposes")

from math import sqrt
from random import randrange

def Num2Text (numbers):
    text = ""
    for number in numbers:
        character = chr(number)
        text = text + character
    return(text)



#########################################
#####  START OF CRYPTOGRAPHIC CODE  #####
#########################################
#Coded using https://gist.github.com/JonCooperWorks/5314103 as a reference

def RandomPrime(cap):
    #Sieve of Eratosthenes using
    #https://www.geeksforgeeks.org/python-program-for-sieve-of-eratosthenes/
    #as a reference implimentation
    #returns the largest random prime before the cap
    
    #creates a list of length cap with all values being True.
    prime = []
    for i in range (0,cap+1):
        prime.append(True)
    
    for itteration in range(2, int(sqrt(cap)+1)):
        if prime[itteration] == True: #if itteration is prime...
            for i in range(itteration*2, cap+1, itteration):
                prime[i] = False #mark all multiples of itteration as not prime
    for itteration in range(cap,0,-1):
        if prime[itteration] == True:
            return(itteration)
    

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
    
    for iteration in range(3, limit, 2):
        #checks odd numbers between 3 and half the value of the number
        #Dev note, upgrade to check 6i - 1 and 6i + 1
        if number % iteration == 0:
            return(False)
    return(True)

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
    T = 1
    OldT = 0
    
    while remainder != 0:
        temp = remainder #temporarily save the remainder...
        quotient, remainder = divmod(OldRemainder, remainder) #...do stuff...
        OldRemainder = temp #... then transfer the previous remainder into OldRemainder
        
        temp = T #temporarily save T ...
        T = OldT - (quotient * T) #...do stuff...
        OldT = temp #... then transfer the pervious S into OldS
        
    return(T)

def GenerateKeypair (p, q):
    Max = p * q
    phi = (p-1) * (q-1) #phi is the totient of n (whatever the #### that means)
    
    # Pick e
    if phi <= 65537:
        return("PickLargerPrimes")
    PublicKey = 65537 #might seem weird but this is what 95.5% of CAs do.
    # https://www.johndcook.com/blog/2018/12/12/rsa-exponent/
    while g != 1:
        PublicKey = randrange(1000,phi) #Randrange is not cryptographically secure. Doesn't need to be.
        g = GreatestCommonDivisor(e,phi)
    
    #calculate the PublicKey
    PrivateKey = MultiplicitveInverse(PrivateKey, phi)
    
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



#######################################
#####  END OF CRYPTOGRAPHIC CODE  #####
#######################################



# cipher = encrypt(83,7471,input())
# print(decrypt(347,7471,cipher))
# print(Num2Text(decrypt(347,7471,cipher)))
print(RandomPrime(10000000))