# Simple example to post an image file to the server
import requests
# url='http://34.123.25.148:8080/upload/image.png'
# files={'image':open('FJR.png','rb')}
# data={"address":"zsb-test.png"}
# r=requests.post(url, data=data, files=files)
url="http://104.197.192.205:8080/upload/image.png"
files={"image":open("ToServer/33.png","rb")}
values={"address":"99.png"}
r=requests.post(url, files=files, data=values)