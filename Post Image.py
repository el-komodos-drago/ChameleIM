# Simple example to post an image file to the server
import requests
url='http://34.123.25.148:8080/upload/image.gif'
files={'image':open('C:\logonew.gif','rb')}
r=requests.post(url, files=files)