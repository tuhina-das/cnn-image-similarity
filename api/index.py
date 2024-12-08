import sys
import os
from flask import Flask
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import base64
from PIL import Image
import io
import math
from math import sqrt
import kagglehub
app = Flask(__name__)


@app.route("/api/python")

def setup():
    print("-------------------------------------------")
    print("                 START OF SETUP             ")
    print("-------------------------------------------")
    print("Python VE: " + sys.executable)
    # base directory to ensure that we start running Python from the same directory
    BASE_DIR = './api/models'
    os.chdir(BASE_DIR)
    # check current directory
    print("Current directory items: ")
    for x in os.listdir("."):
        print(x)
    # embed model
    global embed
    embed = hub.KerasLayer(os.getcwd())
    print("Python confirmed, path embedded, directory checked")
    global cosine_sim_outputs
    cosine_sim_outputs = []
    print("Now, time to test similarity function:")
    os.chdir(os.path.dirname(__file__))
    print(os.getcwd())
    calculate_similarity('./images/black.jpg', './images/galaxywolf.jpg')
    print("-------------------------------------------")
    print("                 END OF SETUP              ")
    print("-------------------------------------------")


# Main script that executes when run
def main(): 
    # first, setting up global variables and testing the cosine sim function (simply just that it' executable)
    setup()
    
    

class TensorVector(object):

    def __init__(self, FileName=None):
        self.FileName = FileName

    def process(self):

        img = tf.io.read_file(self.FileName)
        img = tf.io.decode_jpeg(img, channels=3)
        img = tf.image.resize_with_pad(img, 224, 224)
        img = tf.image.convert_image_dtype(img,tf.float32)[tf.newaxis, ...]
        features = embed(img)
        feature_set = np.squeeze(features)
        return list(feature_set)

def convertBase64(FileName):
    """
    Return the Numpy array for a image
    """
    with open(FileName, "rb") as f:
        data = f.read()

    res = base64.b64encode(data)

    base64data = res.decode("UTF-8")

    imgdata = base64.b64decode(base64data)

    image = Image.open(io.BytesIO(imgdata))

    return np.array(image)

def cosineSim(a1,a2):
    sum = 0
    suma1 = 0
    sumb1 = 0
    for i,j in zip(a1, a2):
        suma1 += i * i
        sumb1 += j*j
        sum += i*j
    cosine_sim = sum / ((sqrt(suma1))*(sqrt(sumb1)))
    return cosine_sim


def calculate_similarity(v1path, v2path):
    # process v1
    helper = TensorVector(v1path)
    vector = helper.process()
    
    # process v2
    helper = TensorVector(v2path)
    vector2 = helper.process()
    
    # Question: How do we get .imshow to display an image?
    plt.imshow(convertBase64(v1path))
    
    output = cosineSim(vector, vector2)
    print(output)
    cosine_sim_outputs.append(output)


if __name__ == "__main__":
    main()
