# captions to images
from PIL import Image, ImageDraw

def create_step(image, caption):
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), caption, fill="white")
    return image
