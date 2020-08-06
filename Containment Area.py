#This is an area to test code.
print("This code was not created by a cryptographic expert and has not been reviewed.")
print("Under no circumstances should it be used for real world perposes")

from math import sqrt

def Num2Text (numbers):
    text = ""
    for number in numbers:
        character = chr(number)
        text = text + character
    return(text)

################################
#####  CRYPTOGRAPHIC CODE  #####
################################

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
    # the number being tested then the result will be larger than the number being tested
    # Note to future me: convert this to use sqrt()
    
    for iteration in range(3, limit, 2):
        #checks odd numbers between 3 and half the value of the number
        

def encrypt(PublicKey, Max, plaintext):
    ciphertext = []
    for character in plaintext: #breaks up plaintext into a series of characters and then for each of them ...
        CharCode = ord(character) #converts the character into it's numeric representation
        CipherChar = (CharCode ** PublicKey) % Max
        # Multiply the numeric representation of the character by itself the number of times
        # specified by the public key, then subtract Max from it until the number left is
        # less than Max.
        ciphertext.append(CipherChar) # Attach the encrypted character to the end of the ciphertext
    return(ciphertext)

def decrypt(PrivateKey, Max, ciphertext):
    plaintext = []
    for character in ciphertext: #breaks up the ciphertext into a series of characters and opperates on each of them indiidually.
        PlainChar = (character ** PrivateKey) % Max
        # Multiply the numeric representation of the character by itself the number of times
        # specified by the public key, then subtract Max from it until the number left is
        # less than Max.
        plaintext.append(PlainChar) # Attach the encrypted character to the end of the plaintext
    return (plaintext)

cipher = encrypt(83,7471,input())
print(decrypt(347,7471,cipher))
print(Num2Text(decrypt(347,7471,cipher)))