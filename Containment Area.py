#This is an area to test code.
print("This code was not created by a cryptographic expert and has not been reviewed.")
print("Under no circumstances should it be used for real world perposes")

def Num2Text (numbers):
    text = ""
    for number in numbers:
        character = chr(number)
        text = text.join(character)
    return(text)

def encrypt(PublicKey, Max, plaintext):
    ciphertext = []
    for character in plaintext: #breaks up plaintext into a series of characters and operates on each of them.
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