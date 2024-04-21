import torch 
from glob import glob 
import pathlib
from os.path import join, basename
import platform
import random 
from PIL import Image
from folders import BASE_FOLDER, INPUT_FOLDER, OUTPUT_FOLDER
from folders import latest_image
from images import process

if platform.system() == 'Windows':
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath



def model(id=None):

    # YOLO should be cloned inside brain folder.
    model_path = str(join(BASE_FOLDER, 'runs\\train\\exp\\weights\\last.pt'))
    yolo_path = str(join(BASE_FOLDER, 'yolov5'))
    # print(f'base folder: {BASE_FOLDER}\ninput folder: {INPUT_FOLDER}\noutput folder: {OUTPUT_FOLDER}\nmodel path: {model_path}')

    model = torch.hub.load(yolo_path, 'custom', path=model_path, source = 'local')

    input_images = glob(join(INPUT_FOLDER, '*.jpg'))

    #TODO: create function taht gets all input images in a folder or from a path 
    # the path could be set to None if you want to process all images in a folder 
    # and return a list of paths, otherwise, return a list with one element, 
    # the element with the specific path you want
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
            img_name = basename(img_path)
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
        print(x1, y1, x2, y2)
        if not id:
            id = random.randint(99,128)
        processed_img_path = str(join(OUTPUT_FOLDER, f'{str(id)}'))
        print(f' processed image path -> {processed_img_path}')
        results.save(save_dir=processed_img_path)
        #boxAndLabel(processed_img_path, img_name, x1, y1, x2, y2, label=f'{issue}\n {confidence}')


        # make id unique and commit to db. 
        # output = [processed_img_path]
        

        #TODO: refactor latest_image
        model_output = {
            'confidence': confidence,
            'issue' : issue,
            'processed_image_url': latest_image(OUTPUT_FOLDER),
        }
        return model_output



if __name__ == '__main__':
    model()
