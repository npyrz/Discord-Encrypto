from firebase import firebase
import requests
import os
from dotenv import load_dotenv
load_dotenv()
firebaseInfo = os.getenv("FIREBASE_DB")
firebase = firebase.FirebaseApplication(firebaseInfo, None)

def messageEncrypter(userKey, username):
    encrypterKey = {
        "A": "`", "B": "~", "C": "!", "D": "@", "E": "#", "F": "$", "G": "%", "H": "^", "I": "&",
        "J": "*", "K": "-", "L": "_", "M": "=", "N": "+", "O": "{", "P": "}", "Q": ";", "R": ":",
        "S": "(", "T": ")", "U": "<", "V": "[", "W": ">", "X": "/", "Y": "?", "Z": "]", "0": "9",
        "1": "8", "2": "7", "3": "6", "4": "5", "5": "4", "6": "3", "7": "2", "8": "1", "9": "0",
        ".": ",", ",": ".", "?": "!", "!": "?", ":": ";", ";": ":", "'": '"', '"': "'", " ": "|"
    }
    encrypted_message = ""
    for char in userKey:
        encrypted_char = encrypterKey.get(char.upper(), char)
        encrypted_message += encrypted_char
    firebase_url = f"{firebaseInfo}Messages/{username}/{userKey}.json"
    requests.put(firebase_url, json=encrypted_message)
    return encrypted_message

def messageDecrypter(get_message, username):
    firebase_url = f"{firebaseInfo}Messages/{username}.json"
    response = requests.get(firebase_url)
    if response.status_code == 200 and response.json() is not None:
        data = response.json()    
        for key, value in data.items():
            if get_message in value:
                del data[key]
                requests.put(firebase_url, json=data)
                return key
        return "The decrypted message you submitted is invalid."
    else:
        return "Does not have data in the database."

def listAllDecrypts(username):
    firebase_url = f"{firebaseInfo}Messages/{username}.json"
    response = requests.get(firebase_url)
    if response.status_code == 200 and response.json() is not None:
        data = response.json()    
        values = list(data.values())
        return "\n".join(values) + "\n"
    else:
        return "You do not have any decryption keys in the database."
    
# ADD USERS TO SEE YOUR ENCRYED MESSAGES | FIX CHECK TO SEE IF THE KEY IS FROM THE USER IF NOT SEND EMEBED
