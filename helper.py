import csv
import math

from multiprocessing import Pool
from PIL import Image, GifImagePlugin

# Gif Load Configuration
GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

# Calculate Length Of Square Image
dataLength = lambda data: int(math.sqrt(len(data)))


# Convert Image To List
def imageToList(filename: str):

    # Open Image In RGBA mode
    image = Image.open(filename).convert("RGBA")

    return list(image.getdata())


# Convert Sequence To Lists
def sequenceToLists(filename: str):
    image = Image.open(filename)

    frames = []
    for i in range(image.n_frames):
        image.seek(i)

        frames.append(list(image.getdata()))

    return frames

# Save Lists As Sequence Image
def listsToSequence(filename: str, data: list, size: tuple):
    base, *images = [listToImage(image, size) for image in data]

    base.save(filename, save_all=True, append_images=images)


# Convert List To Image
def listToImage(data: list, size: tuple):

    # Create Image
    image = Image.new("RGBA", size)
    image.putdata(data)

    return image


# Convert CSV To List
def csvToList(filename: str):

    # Convert String To RGB
    def strToRGB(string: str):
        channels = tuple(map(int, string.split(",")))

        if len(channels) == 1:
            channels *= 3

        return channels

    # Open File
    with open(filename) as file:

        # Ignore Header Line
        file.readline()

        return [strToRGB(item) for item in next(csv.reader(file))]
