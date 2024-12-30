import cv2
import csv
import numpy as np

from math import sqrt

# Calculate Length Of Square Image
dataLength = lambda data: int(sqrt(len(data)))


def imageToArray(filename: str):
    return cv2.imread(filename, cv2.IMREAD_UNCHANGED)


def arrayToImage(filename: str, data):
    cv2.imwrite(filename, data)


def csvToArray(filename: str):

    # Open File
    with open(filename) as file:

        # Ignore Header Line
        file.readline()

        # Process Data
        data = [tuple(map(int, item.split(","))) for item in next(csv.reader(file))]

    # Length Of Image
    length = dataLength(data)

    return np.array(
        [[data[i * length + j] for j in range(length)] for i in range(length)]
    )


def sequencesToArray(filename: str):
    video = cv2.VideoCapture(filename)

    frames = []
    while True:
        status, frame = video.read()

        if status:
            frames.append(frame)
        else:
            break

    return frames
