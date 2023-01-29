import os
import threading
import tinydb
import avif
import logging

# Initialize TinyDB database to keep track of converted photos
db = tinydb.TinyDB("converted_photos.json")
converted_photos = db.table("photos")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("conversion.log"), logging.StreamHandler()]
)


def convert_to_avif(file_path):
    # Get the file name from the file path
    file_name = os.path.basename(file_path)

    # Check if the file has already been converted
    if converted_photos.search(tinydb.where("file_name") == file_name):
        logging.info(f"{file_name} has already been converted.")
        return

    # Open the photo file for reading
    try:
        with open(file_path, "rb") as f:
            image_data = f.read()
    except Exception as e:
        logging.error(f"Error reading {file_name}: {e}")
        return

    # Convert the photo to AVIF format
    try:
        avif_image = avif.encode(image_data, lossless=True)
    except Exception as e:
        logging.error(f"Error encoding {file_name}: {e}")
        return

    # Write the AVIF image to disk
    try:
        with open(os.path.join("/opt/photos/output", file_name + ".avif"), "wb") as f:
            f.write(avif_image)
    except Exception as e:
        logging.error(f"Error writing {file_name}: {e}")
        return

    # Add the photo to the TinyDB database
    converted_photos.insert({"file_name": file_name})
    logging.info(f"Successfully converted {file_name}.")


def main():
    # Get the list of photo files in the input directory
    input_dir = "/opt/photos/input"
    file_paths = [os.path.join(input_dir, file_name) for file_name in os.listdir(input_dir) if
                  file_name.endswith((".png", ".jpg"))]

    # Start a separate thread for each photo
    threads = []
    for file_path in file_paths:
        t = threading.Thread(target=convert_to_avif, args=(file_path,))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
