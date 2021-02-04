import secrets
import os
from PIL import Image
from flaskblog import app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)   # creates a hex patten that's 8 character long
    _, file_extension = os.path.splitext(form_picture.filename)     # returns a tuple of the file name and the extension
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/media/profile_pics', picture_filename)
    # form_picture.save(picture_path)     # save it in it's original size
    # resizing image using the pillow package
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)  # save the image in a resized format
    return picture_filename
