import os
import shutil


def validate_directory_path(directory_path):
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory '{directory_path}' does not exist.")
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Path '{directory_path}' is not a directory.")
    return True


def copy_tree(source_path, destination_path):
    validate_directory_path(source_path)

    if not os.path.exists(destination_path):
        os.makedirs(destination_path, exist_ok=True)

    dir_list = os.listdir(source_path)
    for item in dir_list:
        source_item = os.path.join(source_path, item)
        destination_item = os.path.join(destination_path, item)
        if os.path.isfile(source_item):
            shutil.copy(source_item, destination_item)
        elif os.path.isdir(source_item):
            copy_tree(source_item, destination_item)


def remove_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)


def replace_content(source_path, destination_path):
    validate_directory_path(source_path)
    remove_directory(destination_path)
    os.makedirs(destination_path, exist_ok=True)
    copy_tree(source_path, destination_path)
