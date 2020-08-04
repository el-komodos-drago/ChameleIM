#This is an area to test code.
print("This code was not created by a cryptographic expert and has not been reviewed.")
print("Under no circumstances should it be used for real world perposes")

def encrypt(PublicKey, Max, plaintext):
    ciphertext = []
    for character in plaintext: #breaks up plaintext into a series of characters and operates on each of them.
        CharCode = ord(character) #converts the character into it's numeric representation
        CipherChar = (CharCode ** PublicKey) % Max
        # Multiply the numeric representation of the character by itself the number of times
        # specified by the public key, then subtract Max from it until the number left is
        # less than Max.
        ciphertext.append(CipherChar)
    print(ciphertext)

def decrypt(PrivateKey, Max, plaintext):
    

encrypt(83,7471,input())
