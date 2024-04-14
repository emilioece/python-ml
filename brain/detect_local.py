import torch 
from glob import glob 
import pathlib
from os.path import join, basename
import platform
import random 
from PIL import Image
from folders import BASE_FOLDER, INPUT_FOLDER, OUTPUT_FOLDER
from images import process

if platform.system() == 'Windows':
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath



def model():

    # YOLO should be cloned inside brain folder.
    model_path = str(join(BASE_FOLDER, 'runs\\train\\exp\\weights\\last.pt'))
    yolo_path = str(join(BASE_FOLDER, 'yolov5'))
    print(f'base folder: {BASE_FOLDER}\ninput folder: {INPUT_FOLDER}\noutput folder: {OUTPUT_FOLDER}\nmodel path: {model_path}')

    model = torch.hub.load(yolo_path, 'custom', path=model_path, source = 'local')

    input_images = glob(join(INPUT_FOLDER, '*.jpg'))

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
        
        processed_img_path = str(join(OUTPUT_FOLDER, f'{id}'))
        results.save(save_dir=processed_img_path)
        #boxAndLabel(processed_img_path, img_name, x1, y1, x2, y2, label=f'{issue}\n {confidence}')


        # make id unique and commit to db. 
        # output = [processed_img_path]
        




if __name__ == '__main__':
    model()
