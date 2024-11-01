import os
# Problems?
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd

from dmt_asr.pathing import get_abs_folder_path, get_abs_path

def main():
    base_df = create_base_df()
    base_df_binaries = add_binaries(base_df)

    base_file_path = get_abs_folder_path('all_data_output')
    base_filename = "All_data"
    csv_filename = f"{base_filename}.csv"
    export_df_data(
         df=base_df_binaries,
         file_name=csv_filename,
         base_dir=base_file_path,
         is_csv=True
    )

    json_filename = f"{base_filename}.json"
    export_df_data(
         df=base_df_binaries,
         file_name=json_filename,
         base_dir=base_file_path,
         is_csv=False
    )

    # ref_list_binary, hyp_list_binary = get_binary_lists(base_df_binaries)
    # conf_matrix = create_confusion_matrix(ref_list_binary, hyp_list_binary)
    # export_conf_matrix(base_file_path, conf_matrix)


def read_aligned_file_as_df(file_name):
    file_path = get_abs_path("output", file_name)
    return pd.read_csv(filepath_or_buffer=file_path)

def read_prompt_file(file_name):
    file_path = get_abs_path("files_static", file_name)
    with open(file_path, "r") as fp:
            return [str(line.strip()) for line in fp.readlines()]

def add_binaries(base_df):
     base_df_empty_binaries = add_binary_cols(base_df)
     # base_df_binaries = fill_binary_cols(base_df_empty_binaries) # ADD LATER! Now filler
     base_df_binaries = base_df_empty_binaries
     return base_df_binaries

def fill_binary_cols(base_df_empty_binaries):
     base_df_binaries = fill_binary_values(base_df_empty_binaries)
     return base_df_binaries

# Later: Change how these are determined
def fill_binary_values(base_df_empty_binaries):
     base_df_empty_binaries.loc[base_df_empty_binaries['reference'] != "CORRECTLY_READ", "prompts_plus_orth"] = 1

     base_df_empty_binaries['prompts_plus_hypo'] = base_df_empty_binaries.apply(
          lambda row: 1 if row['prompt'] not in row['hypothesis'] and row['prompt'] not in row['hypothesis_rev'] else 0,
          axis=1)

     return base_df_empty_binaries

def add_binary_cols(base_df):
     base_df.insert(len(base_df.columns), "prompts_plus_orth", 999)
     base_df.insert(len(base_df.columns), "prompts_plus_hypo", 999)
     return base_df


# This is hard-coded
def create_base_df():
    al_df = read_aligned_file_as_df("S01C002V1-filtered-dataframe.csv")
    base_df = pd.DataFrame.from_dict({
        'prompt': read_prompt_file("2LG_words.txt")
    })
    base_df.insert(0, 'id', 'S01C002V12LG')
    base_df = pd.merge(base_df, al_df[['reference', "hypothesis"]], left_index=True, right_index=True)
    return base_df

def export_df_data(df: pd.DataFrame, file_name: str, base_dir: str, is_csv: bool = True):
    file_path = os.path.join(base_dir, file_name)
    if is_csv:
        df.to_csv(file_path, index=False)
    else:
        df.to_json(file_path, index=False)

def get_binary_lists(base_df_binaries):
     ref_list_binary = base_df_binaries["prompts_plus_orth"].tolist()
     hyp_list_binary = base_df_binaries["prompts_plus_hypo"].tolist()
     return ref_list_binary, hyp_list_binary

def create_confusion_matrix(ref_list_binary, hyp_list_binary):
    conf_matrix = confusion_matrix(ref_list_binary,
                          hyp_list_binary)
       
    # cm[0, 0] = TN
    # cm[0, 1] = FP
    # cm[1, 0] = FN
    # cm[1, 1] = TP
    return conf_matrix

def export_conf_matrix(base_dir, conf_matrix):
    file_name = ''
    file_path = os.path.join(base_dir, file_name)
    
    # # Are these useful?
    # descriptions = np.aTN rray([['TN', 'FP'],
    #                          ['FN', 'TP']])
    # conf_matrix_with_desc = np.hstack((descriptions, ))
    
    np.savetxt(file_path, conf_matrix, delimiter=',', fmt='%s')