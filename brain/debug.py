import shutil
from os import listdir, remove
from os.path import join, isdir
from folders import INPUT_FOLDER, OUTPUT_FOLDER, DATABASE_FOLDER
from glob import glob

def clear_directory(directory):
    for item in listdir(directory):
        item_path = join(directory, item)
        if isdir(item_path) and item_path != OUTPUT_FOLDER:
            print(f"Deleting folder: {item_path}")
            try:
                shutil.rmtree(item_path)
            except OSError as e:
                print(f"Error deleting {item_path}: {e}")

def clear_files(directory):
    # Get list of all files in the directory
    files = glob(join(directory, '*'))
    
    # Iterate over each file and remove it
    for file_path in files:
        try:
            remove(file_path)
            print(f"Removed file: {file_path}")
        except Exception as e:
            print(f"Failed to remove file: {file_path}. Error: {e}")
    pass 

def clear_database():
    clear_files(DATABASE_FOLDER)

def clear_input():
    clear_files(INPUT_FOLDER)

def clear_output():
    clear_directory(OUTPUT_FOLDER)

def clear_all():
    clear_output()
    clear_input()
    clear_database()

if __name__ == '__main__':
    clear_all()
