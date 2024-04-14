from os import getcwd, makedirs, listdir
from os.path import exists, join, getmtime, isdir, relpath, dirname
from glob import glob
import json


BASE_FOLDER = getcwd()
INPUT_FOLDER = ''
OUTPUT_FOLDER = ''
INPUT_RELATIVE = 'static\\images'
OUTPUT_RELATIVE = 'static\\processed_images'
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
        STATIC_FOLDER = join(BASE_FOLDER, join('static'))
        
        # Create folders
        config['INPUT_FOLDER'] = create_folder(INPUT_PATH)
        config['OUTPUT_FOLDER'] = create_folder(OUTPUT_PATH)
        config['DATABASE_FOLDER'] = create_folder(DATABASE_PATH)
        config['STATIC_FOLDER'] = create_folder(STATIC_FOLDER)
        
        # Save configuration to JSON file
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

def load_values():
    global BASE_FOLDER, INPUT_FOLDER, OUTPUT_FOLDER, DATABASE_FOLDER, STATIC_FOLDER
    initialize_folders()
    with open(CONFIG_FILE, 'r') as json_file:
        data = json.load(json_file)
    BASE_FOLDER = data['BASE_FOLDER']
    INPUT_FOLDER = data['INPUT_FOLDER']
    OUTPUT_FOLDER = data['OUTPUT_FOLDER']
    DATABASE_FOLDER = data['DATABASE_FOLDER']

def latest_directory(directory:str) -> str:
    # List all sub-directories in directory
    all_subdirs = [join(directory, d) for d in listdir(directory) if isdir(join(directory, d))]
    latest_subdir = max(all_subdirs, key=getmtime)

    # return the last modified one
    # print(latest_subdir)
    return latest_subdir
    
def latest_image(directory: str):
    latest_dir = latest_directory(directory)
    
    if latest_dir:
        latest_image_path = max(glob(join(latest_dir, '*.jpg')), key=getmtime, default=None)
        relative_path = join(OUTPUT_RELATIVE, relpath(latest_image_path, OUTPUT_FOLDER))
        return relative_path
    
    return None


load_values()

if __name__ == '__main__':
    image_path = latest_image(OUTPUT_FOLDER)
    print(image_path)