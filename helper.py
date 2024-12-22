import csv
import math

from PIL import Image

# Calculate Length Of Square Image
dataLength = lambda data: int(math.sqrt(len(data)))


# Convert Image To List
def imageToList(filename: str):

    # Open Image In RGBA mode
    image = Image.open(filename).convert("RGBA")

    return list(image.getdata())


# Convert List To Image
def listToImage(data: list):

    # Create Empty Image
    image = Image.new("RGBA", [dataLength(data)] * 2)

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
