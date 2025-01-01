import os
import cv2
import csv
import numpy as np

from math import sqrt
from quad import QuadTree
from multiprocessing import Pool

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
        data = []

        for item in next(csv.reader(file)):
            values = list(map(int, item.split(",")))

            if len(values) == 1:  # Grayscale
                gray = values[0]
                data.append((gray, gray, gray, 255))

            elif len(values) == 3:  # RGB
                r, g, b = reversed(values)
                data.append((r, g, b, 255))

    # Length Of Image
    length = dataLength(data)

    return [data[i : i + length] for i in range(0, length * length, length)]


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

# Read Limited Number Of Frames
def readFrames(capture, count: int):
    while True:        
        results = []
        for i in range(count):
            status, frame = capture.read()

            if status:
                results.append(frame.tolist())
            else:
                return results

        yield results


# Compress Sequence Of Images
def compressSequence(input: str, size: int, output: str):
    cores = os.cpu_count()
    
    # Capture Video
    cap = cv2.VideoCapture(input)

    # Video File
    out = cv2.VideoWriter(output, cv2.VideoWriter.fourcc(*"mp4v"), cap.get(cv2.CAP_PROP_FPS), (size, size))
    
    with Pool(cores) as pool:
        for frames in readFrames(cap, cores):
            results = pool.starmap(QuadTree.compressData, ([frame, size] for frame in frames))

            for result in results:
                out.write(np.array(result, np.uint8))
                print(".")

    out.release()