import requests
import shutil
import pickle
import os

class PictureLinks:

    def __init__(self):
        self.smallImageSrc = None
        self.fullImage = None

imageLinks = list()

currentDirectory = os.getcwd()

with open("produkty.txt", "rb") as input_file:
    imageLinks = pickle.load(input_file)
counter = 0

folder = 'Zdjeciaa'

try:

    os.mkdir(folder)
except OSError:
        print ("Creation of the directory %s failed" % folder)
else:
        print ("Successfully created the directory %s " % folder)

os.chdir(currentDirectory+'\\'+folder)

for imageLink in imageLinks:
    counter += 1
    print(imageLink.fullImage)

    image_url = imageLink.fullImage
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)
    # Open a local file with wb ( write binary ) permission.
    local_file = open(str(counter)+'.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp

