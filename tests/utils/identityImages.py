# coding=utf-8
import os

script_dir = os.path.dirname(__file__)

RgImages = {
    "front": "identity/identity-front-face.png",
    "back": "identity/identity-back-face.png",
    "selfie": "identity/walter-white.png"
}


def readImage(path):
    file_path = os.path.join(script_dir, path)
    with open(file_path, 'rb') as file:
        return file.read()
