from os import getcwd, makedirs, listdir
from os.path import exists, join, getmtime, isdir, relpath, dirname
from glob import glob
import json


BASE_FOLDER = getcwd()
INPUT_FOLDER = ''
OUTPUT_FOLDER = ''
INPUT_RELATIVE = join('static', 'images')
OUTPUT_RELATIVE = join('static', 'processed_images')
DATABASE_FOLDER = ''


# TODO: hanging config file..
CONFIG_FILE = join(BASE_FOLDER, 'config.json')

def create_folder(folder:str) -> str:
    if not exists(BASE_FOLDER):
        raise FileNotFoundError('Base folder is not defined.')
    if False:     
        print(f'checking if {folder} exists...')
    if not exists(folder):
        print(f'Creating {folder}...')
        makedirs(folder)

    if False:        
        print(f'{folder} exists.')
    return str(join(BASE_FOLDER, folder))

def initialize_folders():
    # If config file doesn't exist, create one with values.
    if not exists(CONFIG_FILE):
        config = {}
        
        # Set base folder
        config['BASE_FOLDER'] = BASE_FOLDER

        INPUT_PATH = join(BASE_FOLDER, INPUT_RELATIVE)
        OUTPUT_PATH = join(BASE_FOLDER, OUTPUT_RELATIVE)
        DATABASE_PATH = join(BASE_FOLDER, join('database'))
        
        # Create folders
        config['INPUT_FOLDER'] = create_folder(INPUT_PATH)
        config['OUTPUT_FOLDER'] = create_folder(OUTPUT_PATH)
        config['DATABASE_FOLDER'] = create_folder(DATABASE_PATH)
        
        # Save configuration to JSON file
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

def load_values():
    global BASE_FOLDER, INPUT_FOLDER, OUTPUT_FOLDER, DATABASE_FOLDER
    initialize_folders()
    with open(CONFIG_FILE, 'r') as json_file:
        data = json.load(json_file)
    BASE_FOLDER = data['BASE_FOLDER']
    INPUT_FOLDER = data['INPUT_FOLDER']
    OUTPUT_FOLDER = data['OUTPUT_FOLDER']
    DATABASE_FOLDER = data['DATABASE_FOLDER']

def latest_directory(directory:str) -> str:
    # List all sub-directories in directory
    all_subdirs = [join(directory, d) for d in listdir
    (directory) if isdir(join(directory, d))]
    
    if not all_subdirs:
        return None
    latest_subdir = max(all_subdirs, key=getmtime)

    # return the last modified one
    
    return latest_subdir
    
def latest_image(img_directory: str):
    # check working directory
    if img_directory == OUTPUT_FOLDER:
        relative_path = OUTPUT_RELATIVE
        abs_path = OUTPUT_FOLDER

    elif(img_directory == INPUT_FOLDER):
    
        relative_path = INPUT_RELATIVE
        abs_path = INPUT_FOLDER
    

    # print(f'relative path ll {relative_path}')
    # print(f'abs path ll {abs_path}')
    # print(f'--- working in {img_directory} ---')
        

    latest_dir = latest_directory(img_directory)
    # works for output since processed image stored in 
    # processed_images/{id}/{img}

    if latest_dir:
        latest_image_path = max(glob(join(latest_dir, '*.jpg')), key=getmtime, default=None)
    else:
        latest_image_path = max(glob(join(INPUT_FOLDER,'*jpg')))

    if latest_image_path:    
        relative_img_path = relpath(latest_image_path, 'static').replace('\\', '/')
        return relative_img_path

    
    return None


load_values()

if __name__ == '__main__':
    image_paths = [INPUT_FOLDER, OUTPUT_FOLDER]
    for image_path in image_paths:
        patha = latest_image(image_path)
        print(patha)