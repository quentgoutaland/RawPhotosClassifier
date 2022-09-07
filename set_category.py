#!/usr/bin/env python3

import tensorflow as tf
import tensorflow.keras.layers as tfl
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import sys
import os
import ProgressBarDecorator as pbd
from pyexif import pyexif
import rawpy
import imageio


def raf_to_jpg(photo):
    """
        make a jpg copy of RAF image (photo) using rawpy to process and imageio to write into new file.
    """
    jpg_name = photo.replace("RAF", "jpg")
    with rawpy.imread(photo) as raw:
        rgb = raw.postprocess()
        imageio.imwrite(jpg_name, rgb)
    return jpg_name


def photo_processing(photo):
    """
        Transform photos to be jpeg and 224x224 to pass through CNN.
    """
    is_a_copy = False
    if photo.endswith("RAF"):
        img = raf_to_jpg(photo)
        is_a_copy = True
    else:
        img = photo
            
    img_jpg = image.load_img(img, target_size=(224, 224))
    x = image.img_to_array(img_jpg)
    x = np.expand_dims(x, axis=0) # correct the dimension of the image otherwise the photos can't be used by tensorflow.
    return x, img, is_a_copy
        

def set_label(photo, category):
    """
        Assign determined category to exif metadata of photo.
    """
    try:
        get_exif = pyexif.ExifEditor(photo)
        get_exif.setTag('ImageDescription', category)
    except:
        print(f"Error: category not added to {photo}")
        
        
@pbd.ProgressBar()
def label_photos(photos):
    """
        Predict category of all photos (list) and assign it to the metadata.
    """
    nb_photos = len(photos)
    for c, photo in enumerate(photos):
        x, img, is_a_copy = photo_processing(photo)
        prediction = category_forecaster.predict(x)
        if is_a_copy == True: 
            os.system(f"rm {img}")
        print(img)
        print(categories)
        print(prediction)
        photo_category = categories[np.argmax(prediction)]
        set_label(photo, photo_category)
        yield (c + 1) / nb_photos # yielded for ProgressBar
  
  

# get current path
path = os.getcwd()

#load trained NN to recognize category of photo
category_forecaster = tf.keras.models.load_model('/home/sheadhrethil/Projects/PhotosClassifier/photos_classifier')


# Gather all photos in current directory
photos = [filename for filename in os.listdir(path)]

#photo's possible categories
categories = ['animal',
'architecture',
'astrophotography',
'landscape',
'macrophotography',
'portrait',
'sport',
'object & food',
'transport',
'street photography']

label_photos(photos)

        
    
    
