from PIL import Image


# Convert Image To List
def imageToList(filename: str):
    image = Image.open(filename)

    # Grayscale Conversion
    image = image.convert("L")

    return list(image.getdata())


# Convert CSV To List
def csvToList(filename: str):
    with open(filename) as file:

        # Ignore First Line
        file.readline()

        data = file.readline().split(",")

    return list(map(int, data))
