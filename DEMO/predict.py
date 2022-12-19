import os
import cv2
import shutil
import eel
import cv2
import tensorflow as tf
from keras.models import model_from_json
import numpy as np

#NUMEROID DIAGNOSTICO Y NUMERO DE FRAME
AVIS = "./AVI_organized/"
EXTRACTED_FRAMES = "./DEMO/video_frames"
ILL_FRAMES = "./ill_frames"

def predict(folder_name):

  frame_names = os.listdir(folder_name)
  SIZE = 350
  model = load_model()

  total_num_frames = len(frame_names)
  count = 0

  for frame_name in frame_names:
    img = cv2.imread(folder_name + '/' + frame_name, cv2.IMREAD_GRAYSCALE) / 255
    img = cv2.resize(img, (SIZE, SIZE), interpolation = cv2.INTER_AREA)
    img = tf.reshape(img, shape=(SIZE, SIZE, 1))
    count += round(model.predict(np.array([img]))[0, 0])

  return int(round(100*(count/total_num_frames)))

def load_model(): # Canviar paths!!
  #Loading model and weights
  json_file = open('DEMO/models/95-1003-995_W2_lr0.05model.json','r')
  model_json = json_file.read()
  json_file.close()
  model = model_from_json(model_json)
  model.load_weights('DEMO/models/95-1003-995_W2_lr0.05weights.hdf5')
  return model

def extract_frames(input_path, destination_folder,hasHypertrophy):
    # Open the video file
    vidcap = cv2.VideoCapture(input_path)

    # Read the video file frame by frame
    success, frame = vidcap.read()
    count = 0
    while success:
        # Save the frame as an image file
        cv2.imwrite(f"{destination_folder}/{count}.jpg", frame)

        # Read the next frame
        success, frame = vidcap.read()
        count += 1

@eel.expose
def process(video_path):
    
    # Remove the folders if they exist
    if os.path.exists(EXTRACTED_FRAMES):
        shutil.rmtree(EXTRACTED_FRAMES)

    # Create the folders again
    os.mkdir(EXTRACTED_FRAMES)
    video_path = "DEMO/videos_demo/" + video_path
    extract_frames(video_path,EXTRACTED_FRAMES,0)
    load_model()
    result = predict(EXTRACTED_FRAMES)
    return result

dirname = os.path.dirname(__file__)
eel.init(os.path.join(dirname, "web/"))
eel.start("index4.html")