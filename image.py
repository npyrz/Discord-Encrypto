from firebase import firebase
import requests
import cv2
from io import BytesIO
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
firebaseInfo = os.getenv("FIREBASE_DB")
firebase = firebase.FirebaseApplication(firebaseInfo, None)

def imageEncrypter(image_url, username):
    response = requests.get(image_url)
    img_data = BytesIO(response.content)
    img_rgb = mpimg.imread(img_data)[...,:3]
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    noise = np.random.normal(loc=0, scale=10, size=img_gray.shape).astype(np.uint8)
    img_gray = img_gray.astype(np.uint8)
    img_noisy = cv2.add(img_gray, noise)
    img_blurred = cv2.GaussianBlur(img_noisy, (15, 15), 0)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"{timestamp}"
    img = Image.fromarray(img_blurred)
    img.save(os.path.join("imgs", file_name + ".png"))
    firebase_url = f"{firebaseInfo}Images/{username}/{file_name}.json"
    requests.put(firebase_url, json=image_url)
    return file_name

def imageDecrypter(encrypted_photo, username):
    firebase_url = f"{firebaseInfo}Images/{username}.json"
    response = requests.get(firebase_url)

    if response.status_code == 200 and response.json() is not None:
        data = response.json()    
        for key, value in data.items():
            if encrypted_photo in key:
                del data[key]
                requests.put(firebase_url, json=data)
                img_path = os.path.join("imgs", f"{encrypted_photo}.png")
                if os.path.exists(img_path):
                    os.remove(img_path)
                return value
        return "ERROR"
    else:
        return "ERROR"

def listAllKeys(username):
    firebase_url = f"{firebaseInfo}Images/{username}.json"
    response = requests.get(firebase_url)
    if response.status_code == 200 and response.json() is not None:
        data = response.json()    
        keys = list(data.keys())
        return "\n".join(keys) + "\n"

    else:
        return "You do not have any decryption keys in the database."

# ADD USERS TO SEE YOUR ENCRYED MESSAGES | FIX CHECK TO SEE IF THE KEY IS FROM THE USER IF NOT SEND EMEBED