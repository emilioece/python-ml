import torch 
from glob import glob 
import pathlib
from os import getcwd, path
import platform

if platform.system() == 'Windows':
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

def model():
    # TODO: Create folders if they don't exist...
    BASE_FOLDER = getcwd()
    INPUT_FOLDER = str(path.join(BASE_FOLDER, 'static\\images\\'))
    OUTPUT_FOLDER = str(path.join(BASE_FOLDER, 'static\\processed_images\\'))

    model_path = str(path.join(BASE_FOLDER, 'runs\\train\\exp\\weights\\best.pt'))
    yolo_path = str(path.join(BASE_FOLDER, 'yolov5'))
    print(f'base folder: {BASE_FOLDER}\ninput folder: {INPUT_FOLDER}\noutput folder: {OUTPUT_FOLDER}\nmodel path: {model_path}')

    model = torch.hub.load(yolo_path, 'custom', path=model_path, source = 'local')

    input_images = glob(path.join(INPUT_FOLDER, '*.jpg'))

    if not input_images:
        print("No images found in the input folder. Check the path or file extensions.")
    else:
        confidence = ''
        issue = ''
        # Run inference
        results = model(input_images)

        # Access class names
        class_names = model.module.names if hasattr(model, 'module') else model.names

        # Process each detection
        for img_path, img_detections in zip(input_images, results.pred):
            print(f"Detections for {img_path}:")
            for *box, conf, cls_id in img_detections:
                x1, y1, x2, y2 = box
                # Use cls_id to get the class name
                class_name = class_names[int(cls_id)]
                confidence = f"Confidence: {conf:.2f}"
                issue = f"Class: {class_name}"

        # Saving processed images to the specified output directory
        # We use 'save_dir' to directly specify the output folder
        results.save(save_dir=str(OUTPUT_FOLDER))



if __name__ == '__main__':
    model()
