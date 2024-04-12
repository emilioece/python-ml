from os import getcwd, makedirs
from os.path import exists, join


def create_folder(folder:str) -> str:
    if not exists(BASE_FOLDER):
        raise FileNotFoundError('Base folder is not defined.')
        
    print(f'checking if {folder} exists...')
    if not exists(folder):
        print(f'Creating {folder}...')
        makedirs(folder)
        
    print(f'{folder} exists.')
    return str(join(BASE_FOLDER, folder))




BASE_FOLDER = getcwd()
INPUT_FOLDER = create_folder('static\\images\\')
OUTPUT_FOLDER = create_folder('static\\processed_images\\')


