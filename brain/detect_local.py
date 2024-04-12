import torch 
from glob import glob 
import pathlib
from os import getcwd, path
import platform
import random 
from PIL import Image
from folders import BASE_FOLDER, INPUT_FOLDER, OUTPUT_FOLDER


if platform.system() == 'Windows':
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

def process(folder_path:str, new_size = (640, 640)) -> str:
    # Use glob to find all image files in the folder
    image_files = glob(path.join(folder_path, '*.*'))

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

def model():

    # YOLO should be cloned inside brain folder.
    model_path = str(path.join(BASE_FOLDER, 'runs\\train\\exp\\weights\\last.pt'))
    yolo_path = str(path.join(BASE_FOLDER, 'yolov5'))
    print(f'base folder: {BASE_FOLDER}\ninput folder: {INPUT_FOLDER}\noutput folder: {OUTPUT_FOLDER}\nmodel path: {model_path}')

    model = torch.hub.load(yolo_path, 'custom', path=model_path, source = 'local')

    input_images = glob(path.join(INPUT_FOLDER, '*.jpg'))

    if not input_images:
        print("No images found in the input folder. Check the path or file extensions.")
    else:
        process(INPUT_FOLDER)
        confidence = ''
        issue = ''
        # Run inference
        results = model(input_images)
        # Access class names
        class_names = model.module.names if hasattr(model, 'module') else model.names

        # Process each detection
        for img_path, img_detections in zip(input_images, results.pred):
            id = random.randint(100, 300)
            img_name = path.basename(img_path)
            print(f"Detections for {img_path}:")
            for *box, conf, cls_id in img_detections:
                x1, y1, x2, y2 = box
                # Use cls_id to get the class name
                class_name = class_names[int(cls_id)]
                confidence = f"Confidence: {conf:.2f}"
                issue = f"Class: {class_name}"


            # Saving processed images to the specified output directory
            # We use 'save_dir' to directly specify the output folder
        # TODO: Save to patients name
        results.save(save_dir=str(path.join(OUTPUT_FOLDER, f'{id}')))
        




if __name__ == '__main__':
    model()
