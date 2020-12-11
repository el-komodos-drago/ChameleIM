from Cryptography import Hash
import sqlite3
import requests
import os
import json
import base64

#see https://requests.readthedocs.io/en/master/user/authentication/ for authentication details

def RegisterPublicKey():
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read() #Save the contents of the WiFall Key file to WFK
    KHash,salt = Hash(WFK) #get the hash and salt by Hashing it
    
    url="http://104.197.192.205:8080/register"
    KHash = base64.b64encode(KHash.encode('utf-8')).decode('ascii')
    data={"password":KHash}
    #print(data)
    r=requests.post(url, data=data)
    PublicKeyID = int(r.text)
    return(PublicKeyID,salt)

def SendImage(image,MessageID,PublicKeyID):
    #This sends an image to the server addressed to the provided PublicKeyID
    
    #Based upon https://github.com/jumbry/Flask-fileserver/blob/main/postimage.py
    FileName = "ToServer/"+str(MessageID)+".png"
    image.save(FileName)
    
    url="http://104.197.192.205:8080/upload/ChameleIM.png"
    with open(FileName,'rb') as image:
        files={"image":image} # Put the image in a dictionary
        data={"address":PublicKeyID} # Put the PublicKeyID in a dictionary labelled as address
        r=requests.post(url, files=files, data=data) # Sends those dictionaries to the server
    os.remove(FileName)
    print("Done")

def GetImageList(PublicKeyID,KHash):
    KHash = base64.b64encode(KHash.encode('utf-8')).decode('ascii')
    url="http://104.197.192.205:8080/DownloadList"
    response=requests.get(url, auth=(PublicKeyID,KHash))
    return(response.text)

def GetImage(filename,PublicKeyID,KHash):
    KHash = base64.b64encode(KHash.encode('utf-8')).decode('ascii') # Encode KHash as base64
    url="http://104.197.192.205:8080/OpenImage"
    print(filename)
    data = {"filename":filename}
    response=requests.post(url, auth=(PublicKeyID,KHash), data=data) # Sends the request
    #to the server with the filename and the authentication.
    return(response.content) # Return the binary for the image

def DeleteImage(filename,PublicKeyID,KHash):
    KHash = base64.b64encode(KHash.encode('utf-8')).decode('ascii')
    url="http://104.197.192.205:8080/delete"
    data = {"filename":filename}
    response=requests.post(url, auth=(PublicKeyID,KHash), data=data)
    return()


    
