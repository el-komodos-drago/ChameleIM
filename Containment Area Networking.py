from Cryptography import Hash
import sqlite3
import requests
import os
import json
import base64

def RegisterPublicKey():
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read() #Save the contents of the WiFall Key file to WFK
    KHash,salt = Hash(WFK) #get the hash and salt by Hashing it
    
    url="http://104.197.192.205:8080/register"
    KHash = base64.b64encode(KHash.encode('utf-8')).decode('ascii')
    print(KHash)
    data={"password":KHash}
    #print(data)
    r=requests.post(url, data=data)
    PublicKeyID = int(r.text)
    return(PublicKeyID,salt)

#image,MessageID
def SendImage(FileName,PublicKeyID):  #image,MessageID
    #Based upon https://github.com/jumbry/Flask-fileserver/blob/main/postimage.py
    #FileName = "ToServer/"+str(MessageID)+".png"
    #image.save(FileName)
    
    url="http://104.197.192.205:8080/upload/ChameleIM.png"
    with open(FileName,'rb') as image:
        files={"image":image}
        data={"address":PublicKeyID}
        r=requests.post(url, files=files, data=data)
    #os.remove(FileName)
    print("Done")

def GetImageList(PublicKeyID,KHash):
    url="http://104.197.192.205:8080/DownloadList"
    print(PublicKeyID,KHash)
    response=requests.get(url, auth=(PublicKeyID,KHash))
    return(response.text)

def GetImage(filename,PublicKeyID,KHash):
    url="http://104.197.192.205:8080/OpenImage"
    data = {"filename":filename}
    print(filename,PublicKeyID,KHash)
    response=requests.post(url, auth=(PublicKeyID,KHash), data=data)
    print(response.text)
    return(response.content)

def DeleteImage(filename,PublicKeyID,KHash):
    url="http://104.197.192.205:8080/delete"
    data = {"filename":filename}
    response=requests.post(url, auth=(PublicKeyID,KHash), data=data)
    return()

def CalcKHash(salt):
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read()
    KHash = Hash(WFK,salt)
    return(KHash)

MessageID = 10

PublicKeyID, salt = RegisterPublicKey()
print(PublicKeyID)
SendImage("ToServer/FJR.png",PublicKeyID)
KHash = CalcKHash(salt)[0]
KHash = base64.b64encode(KHash.encode('utf-8')).decode('ascii')
print()
result = GetImageList(PublicKeyID,KHash)
images = json.loads(result)
print(images)
for image in images:
    with open("Messages/"+str(MessageID)+".png","wb") as file:
        response = GetImage(image,PublicKeyID,KHash)
        input()
        file.write(response)