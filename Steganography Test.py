#Run in directory with any file called Thing.png
from stegano import lsb
SecretData="W£m	-‰æäÖ^"
lsb.hide("Thing.png",SecretData).save("Thing.png")
SecretData2 = lsb.reveal("Thing.png")
print(SecretData2)
if SecretData != SecretData2:
    print("You shouldn't be seeing this")
input("Press enter to close program")