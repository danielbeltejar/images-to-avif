import os
from concurrent.futures import ThreadPoolExecutor
import logging

from picture import Picture

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("conversion.log"), logging.StreamHandler()]
)


def main():
    # Get the list of photo files in the input directory
    input_dir = "/opt/images-to-avif/input"

    # Get a list of all image files in the input directory and its subdirectories
    file_paths = []
    extension = (".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".heic", ".HEIC", ".heif", ".HEIF")
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(tuple(extension)):
                file_paths.append(os.path.join(root, file))

    # Start a separate thread for each photo
    with ThreadPoolExecutor(max_workers=8) as executor:
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            logging.info(f"Conversion for {file_name} has started.")
            executor.submit(Picture, file_path)


if __name__ == "__main__":
    main()
