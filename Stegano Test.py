#Run in directory with any file called Thing.png
from steganography.steganography import Steganography
SecretData="W£m	-‰æäÖ^"
SecretData="Stuff"
Steganography.encode("Thing.png", "Thing.png", SecretData)
SecretData2=Steganography.decode("Thing.png")
print(SecretData2)
if SecretData != SecretData2:
    print("You shouldn't be seeing this")
input("Press enter to close program")