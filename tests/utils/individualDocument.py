# coding=utf-8

RgImages = {
    "front": "../utils/identity/rg-front-face.png",
    "back": "../utils/identity/rg-back-face.png",
    "selfie": "../utils/identity/walter-white.png"
}


def readImage(path):
    with open(path, 'rb') as file:
        return file.read()
