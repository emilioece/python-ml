from glob import glob
from os.path import join
from PIL import Image


def process(folder_path:str, new_size = (640, 640)) -> str:
    # Use glob to find all image files in the folder
    image_files = glob(join(folder_path, '*.*'))

    # Iterate over each image file
    for file_path in image_files:
        # Check if the file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Open the image
            with Image.open(file_path) as img:
                # Resize the image
                resized_img = img.resize(new_size)
                # Overwrite the original image with the resized one
                resized_img.save(file_path)