import shutil
from os import listdir
from os.path import join, isdir
from folders import OUTPUT_FOLDER

def clear_directory(directory):
    for item in listdir(directory):
        item_path = join(directory, item)
        if isdir(item_path) and item_path != OUTPUT_FOLDER:
            print(f"Deleting folder: {item_path}")
            try:
                shutil.rmtree(item_path)
            except OSError as e:
                print(f"Error deleting {item_path}: {e}")
    
def clear_output():
    clear_directory(OUTPUT_FOLDER)

if __name__ == '__main__':
    clear_output()
