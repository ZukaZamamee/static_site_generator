import os
import shutil

def clean_directory(dir_path):
    try:
        if os.path.isdir(dir_path):
            print(f"Deleting directory at {dir_path}")
            shutil.rmtree(dir_path)
    except Exception as e:
        raise Exception(f"Error {e} encountered while trying to delete directory at {dir_path}")

def copy_files_recursive(source_dir_path, dest_dir_path):
    #Check if destination directory exists, create if not
    try:
        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path, exist_ok=True)

        print("Copying Files:")
        for filename in os.listdir(source_dir_path):
            from_path = os.path.join(source_dir_path, filename)
            dest_path = os.path.join(dest_dir_path, filename)
            print(f" * {from_path} -> {dest_path}")
            #If path points to a file, copy file from source to destination
            if os.path.isfile(from_path):
                shutil.copy(from_path, dest_path)
            #Call function recursively if directory
            else:
                copy_files_recursive(from_path, dest_path)
    except Exception as e:
        raise Exception(f"Error {e} encountered while trying to copy files from {source_dir_path} to {dest_dir_path}")