from random import randint
from django.core.mail import EmailMessage
from datetime import datetime
from PIL import Image
import requests
import os
import pdb


def get_image_name():
    image_name = 'IMG_'+ datetime.now().strftime('%Y%m%d_%H%M%S')
    return image_name

def store_orignal_image(url, name):

    image = requests.get(url)
    file_name = os.getcwd() +  "/user/orignal_images/"  + name
    orignal_file = open(file_name, "wb")
    orignal_file.write(image.content)
    orignal_file.close()
    return file_name

    
def compress_image(image, name):
    
    compress_image = Image.open(image)
    if compress_image.height > 50 or compress_image.width > 50:
        output_size = (200, 200)
        compress_image.thumbnail(output_size)
        file_path = os.getcwd() +  "/user/compress_images/"  + name
        compress_image.save(file_path)
    return file_path
