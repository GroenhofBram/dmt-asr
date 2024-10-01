from dmt_asr.islinux import is_linux
from dmt_asr.pathing import get_abs_folder_path

LINUX_BASE_DIR = "/vol/bigdata/corpora/CHOREC-1.0/data"
WINDOWS_BASE_DIR = get_abs_folder_path("files\\Data")

def get_base_dir_for_generalised_path():
    if is_linux():
        print("LINUX_BASE_DIR is undefined, change this when location is known in generalisedbasedir.py")
        return LINUX_BASE_DIR
    # print(f"BASE DIRECTORY WINDOWS:\n \t {WINDOWS_BASE_DIR}")
    return f"{WINDOWS_BASE_DIR}"