import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import base64
from PIL import Image
import io
from math import sqrt
from retail_detection import get_retail_detection, get_image_embedding
# Removing matplotlib and pandas since they're not used 

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(BASE_DIR, 'models')
parent_dir = os.path.dirname(os.path.abspath(__file__))

# Keyword detection/assignment w/ Cursor's help lol
# ------------------------------------------------------------------------------------------------  
# loading TF model
global embed
embed = hub.KerasLayer(parent_dir + "/models")

# importing CLIP models and categories from retail_detection
# from retail_detection import (
#     clip_model,
#     clip_processor, 
#     RETAIL_CATEGORIES,
#     get_retail_detection
# )

# @app.route("/api/detect", methods=['POST'])
# # NTS TO GO BACK HERE AND WRIT WHAT THIS IS
# def detect_items():
#     # getting image path from frontend's POST request (if one is made)
#     data = request.get_json()
#     image_path = '../public' + data.get('image_path')
    
#     try:
#         # calls the get_retail_detection function from retail_detection.py
#         results = get_retail_detection(image_path)
#         detections = results['detections']
        
#         # Check for suspicious activity -- NTS to go back here and delete this, because it's unnecessary
#         suspicious = any(
#             d["confidence"] > 0.6 and 
#             d["category"] in [
#                 "person concealing item",
#                 "group of people", 
#                 "security tag"
#             ]
#             for d in detections
#         )
        
#         # should return keywords for the given image
#         return jsonify({
#             "detections": detections,
#             "suspicious": suspicious
#         }), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
# # ------------------------------------------------------------------------------------------------  

# Image detection code for OW
@app.route("/backend/api/app", methods=['POST'])
def receive_data():
    data = request.get_json()
    v1path = '../../public' + data.get('string1')
    v2path = '../../public' + data.get('string2')
    
    similarity_value = str(calculate_similarity(v1path, v2path))
    print("we got here!")
    
    response = {
        "response": similarity_value
    }
    return jsonify(response), 200  # Return a 200 OK status
    
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
    # plt.imshow(convertBase64(v1path))
    
    return cosineSim(vector, vector2)
    # Commented out for testing
    # return cosine_sim_outputs.append(output)

if __name__ == "__main__":
    app.run()
