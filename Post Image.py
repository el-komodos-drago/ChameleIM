# Simple example to post an image file to the server
import requests
url='http://34.123.25.148:8080/upload/image.png'
files={'image':open('Sample.png','rb')}
r=requests.post(url, files=files)