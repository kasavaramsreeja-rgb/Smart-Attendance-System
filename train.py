import cv2
import numpy as np
from PIL import Image
import os

path = 'dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for image_path in image_paths:
        gray_img = Image.open(image_path).convert('L')
        img_arr = np.array(gray_img, 'uint8')

        id = int(os.path.split(image_path)[-1].split(".")[1])

        face_samples.append(img_arr)
        ids.append(id)

    return face_samples, ids

faces, ids = get_images_and_labels(path)

print("Training faces... Please wait")

recognizer.train(faces, np.array(ids))
recognizer.save('trainer/trainer.yml')

print("Training completed!")