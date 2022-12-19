import pydicom
import os
import cv2
import shutil
#NUMEROID DIAGNOSTICO Y NUMERO DE FRAME
AVIS = "./AVI_organized/"
HEALTHY_FRAMES = "./healthy_frames"
ILL_FRAMES = "./ill_frames"

def generate_name(path,i,hasHypertrophy):
    # print(path)
    path_chunks = path.split("/")
    aux = path_chunks[-1].split("_")
    axis = aux[-1].split(".")[0]
    # print("pathchunks",path_chunks)
    return f"{path_chunks[-3]}_{i}_{hasHypertrophy}_{aux[-2]}_{axis}.jpg"

def extract_frames(input_path, destination_folder,hasHypertrophy):
    # Open the video file
    vidcap = cv2.VideoCapture(input_path)

    # Read the video file frame by frame
    success, frame = vidcap.read()
    count = 0
    while success:
        # Save the frame as an image file
        cv2.imwrite(f"{destination_folder}/{generate_name(input_path,count,hasHypertrophy)}", frame)

        # Read the next frame
        success, frame = vidcap.read()
        count += 1

def preprocess_data(patient_path,destination_folder,hasHypertrophy):
    W2_PATH = "/2W/"
    # W0_PATH = "/0W/"

    week2_video_paths = os.listdir(patient_path+W2_PATH)
    # week0_video_paths = os.listdir(patient_path+W0_PATH)
   
    for video in week2_video_paths:
        # print("el name del video: ",video)
        extract_frames(patient_path+W2_PATH+video, destination_folder,hasHypertrophy)


# Remove the folders if they exist
if os.path.exists(HEALTHY_FRAMES):
    shutil.rmtree(HEALTHY_FRAMES)
if os.path.exists(ILL_FRAMES):
    shutil.rmtree(ILL_FRAMES)

# Create the folders again
os.mkdir(HEALTHY_FRAMES)
os.mkdir(ILL_FRAMES)

healthies = os.listdir(AVIS+"healthy")
ills = os.listdir(AVIS+"ill")
# print(patients)
for patient in healthies:
    patient_path = AVIS+"healthy/"+patient
    preprocess_data(patient_path,HEALTHY_FRAMES,0)

for patient in ills:
    patient_path = AVIS+"ill/"+patient
    preprocess_data(patient_path,ILL_FRAMES,1)


    
