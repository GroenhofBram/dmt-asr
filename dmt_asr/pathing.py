from os.path import abspath, dirname, join

def get_abs_path(base_path: str, file_name: str):
    current_file_path = dirname(__file__)
    joined_paths = join(current_file_path, "..", base_path, file_name)
    return abspath(joined_paths)

def get_abs_folder_path(folder_name: str):
    base_path = dirname(__file__)
    #print(f"base: {base_path}")
    joined_folder = join(base_path, '..', folder_name)
    #print(f"joined: {joined_folder}")
    return abspath(joined_folder)

def get_base_dir_folder_path(folder_name: str, model_name: str, VAD_decision: str):
    if VAD_decision == "y":
        model_name = model_name + "_VAD"
        base_path = dirname(__file__)
        #print(f"base: {base_path}")
        joined_folder = join(base_path, '..', folder_name, model_name)
        return abspath(joined_folder)
    else:
        base_path = dirname(__file__)
        #print(f"base: {base_path}")
        joined_folder = join(base_path, '..', folder_name, model_name)
        return abspath(joined_folder)
