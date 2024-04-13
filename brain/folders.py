from os import getcwd, makedirs
from os.path import exists, join
import json


BASE_FOLDER = getcwd()
INPUT_FOLDER = ''
OUTPUT_FOLDER = ''
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

        INPUT_PATH = join(BASE_FOLDER, 'static/images')
        OUTPUT_PATH = join(BASE_FOLDER, 'static/processed_images')
        DATABASE_PATH = join(BASE_FOLDER, 'database')
        
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


load_values()


