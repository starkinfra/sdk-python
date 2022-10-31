# coding=utf-8

RgImages = {
    "front": "../utils/identity/identity-front-face.png",
    "back": "../utils/identity/identity-back-face.png",
    "selfie": "../utils/identity/walter-white.png"
}


def readImage(path):
    with open(path, 'rb') as file:
        return file.read()
