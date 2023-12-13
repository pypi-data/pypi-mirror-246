import os
import shutil

def find_directory(root_path, target_dir_name):
    for root, dirs, _ in os.walk(root_path):
        if target_dir_name in dirs:
            return os.path.join(root, target_dir_name)
    return None

def find_and_replace_file(root_path, target_file_name, replacement_file_path):
    """
    Searches for a file in the file system and replaces it with another file.

    :param root_path: The directory path where the search should begin.
    :param target_file_name: The name of the file to be replaced.
    :param replacement_file_path: The path to the file that will replace the target file.
    """
    for root, dirs, files in os.walk(root_path):
        if target_file_name in files:
            target_file_path = os.path.join(root, target_file_name)
            print(f"Found target file at: {target_file_path}")
            try:
                shutil.copy(replacement_file_path, target_file_path)
                print(f"Successfully replaced {target_file_path} with {replacement_file_path}")
            except Exception as e:
                print(f"Error replacing file: {e}")
            break
    else:
        print("Target file not found.")


def inject_main():
    root_path = '/'
    target_dir_name = 'LlamaIndex'
    path_to_llama_index = find_directory(root_path, target_dir_name)
    if path_to_llama_index:
        print(f"LlamaIndex found at: {path_to_llama_index}")
    else:
        print("LlamaIndex not found.")
        return

    # target_file_name = 'openai.py'
    # replacement_file_path = 'sigiq/openai.py'
    # find_and_replace_file(path_to_llama_index, target_file_name, replacement_file_path)
