import os
import wget
import re
from PIL import Image


def download_file(url, destination_folder):
    file_name = wget.download(url, out=destination_folder)
    return file_name


def delete_file(file_path):
    os.remove(file_path)


def convert_to_jpeg(file_path):
    if file_path.endswith('.png'):
        image = Image.open(file_path)
        new_file_path = re.sub('.png$', '.jpg', file_path)
        image.save(new_file_path, "JPEG")
        delete_file(file_path)
        return new_file_path
    return file_path


def fix_aspect_ratio(file_path):
    image = Image.open(file_path)
    width = image.size[0]
    height = image.size[1]
    minimum_height = int(width / 1.9)  # 1.9 aspect ratio must be maintained for landscape images
    minimum_width = int(height / 1.0)  # portrait photos should be squared
    if width > height and height < minimum_height:
        background = Image.new('RGBA', (width, minimum_height), (255, 255, 255, 255))
        background.paste(image, (0, minimum_height / 2 - height / 2), image.convert('RGBA'))
        background.save(file_path)
    elif height > width and width < minimum_width:
        background = Image.new('RGBA', (minimum_width, height), (255, 255, 255, 255))
        background.paste(image, (minimum_width / 2 - width / 2, 0), image.convert('RGBA'))
        background.save(file_path)
