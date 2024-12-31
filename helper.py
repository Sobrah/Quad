import cv2
import csv
import numpy as np


from math import sqrt

# Calculate Length Of Square Image
dataLength = lambda data: int(sqrt(len(data)))


# Convert Image To List
def imageToList(filename: str):
    return cv2.imread(filename, cv2.IMREAD_UNCHANGED).tolist()


# Convert List To Image
def listToImage(filename: str, data: list):
    cv2.imwrite(filename, np.array(data))


# Convert CSV File To List
def csvToList(filename: str):

    # Open File
    with open(filename) as file:

        # Ignore Header Line
        file.readline()

        # Process Data
        data = [tuple(map(int, item.split(","))) for item in next(csv.reader(file))]

    # Length Of Image
    length = dataLength(data)

    return [[data[i * length + j] for j in range(length)] for i in range(length)]


# Convert Sequence To Lists
def sequenceToLists(filename: str):
    video = cv2.VideoCapture(filename)

    frames = []
    while True:
        status, frame = video.read()

        if status:
            frames.append(frame.tolist())
        else:
            break

    return frames


# Convert Lists To Sequence
def listsToSequence(filename: str, fourcc: str, fps: int, data: list):

    # Create Empty Video
    video = cv2.VideoWriter(
        filename, cv2.VideoWriter.fourcc(*fourcc), fps, (len(data[0][0]), len(data[0]))
    )

    for frame in np.array(data, np.uint8):
        video.write(frame)

    video.release()
