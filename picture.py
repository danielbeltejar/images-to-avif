import logging
import os
import time

from PIL import Image
from PIL.Image import Exif
from pillow_heif import register_heif_opener

from utils.pretty_file_size import get_pretty_file_size

register_heif_opener()


class Picture(object):
    input_image_data: Image.Image
    picture_file_path: str
    picture_file_name: str
    exif_data: Exif

    def __init__(self, file_path):
        self.picture_file_path = file_path

        # Get the data from the original image
        self.input_image_data = Image.open(self.picture_file_path)

        # Get the EXIF data from the image
        self.exif_data = self.input_image_data.getexif()

        # Get the file name from the file path
        self.picture_file_name = os.path.basename(self.picture_file_path)

        # Remove the original extension of the file
        extensions = [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".heic", ".HEIC", ".heif", ".HEIF"]
        for ext in extensions:
            self.picture_file_name = self.picture_file_name.replace(ext, "")
            break

        self.convert()

    def convert(self):
        start_time = time.time()

        try:
            self.input_image_data.save(os.path.join("/opt/photoprism/originals/", self.picture_file_name + ".avif"),
                                       'avif',
                                       qmin=0,
                                       qmax=63,
                                       optimize=True,
                                       exif=self.exif_data)
        except Exception as e:
            logging.error(f"Error processing {self.picture_file_name}: {e}")
            return

        logging.info(f"Successfully converted {self.picture_file_name} in {(time.time() - start_time) * 1000:.2f} ms. ( {get_pretty_file_size(self.picture_file_path)} > {get_pretty_file_size('/opt/photoprism/originals/' + self.picture_file_name + '.avif')})")

        # Removes input file from the import folder
        os.remove(self.picture_file_path)

        del self
