import os
import glob
import pandas as pd

def main():
    output_dir = get_output_dir()
    print(f"Output directory: {output_dir}") 
    CHOREC_files = get_CHOREC_files(output_dir)
    w2v2_df, fw2_df = get_dfs(CHOREC_files)
    reformat_dfs(w2v2_df, fw2_df, output_dir)


def get_output_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    output_dir = os.path.join(parent_dir, "output")
    return output_dir

def get_CHOREC_files(output_dir):
    file_pattern = os.path.join(output_dir, "CHOREC*.csv")
    chorec_files = glob.glob(file_pattern)
    print(f"------------------\nFiles found: {chorec_files}\n\tNumber of files: {len(chorec_files)}\n------------------") 
    return chorec_files

def get_dfs(CHOREC_files):
    for file_path in CHOREC_files:
        if "Whisper" in file_path:
            fw2_file_path = file_path
        elif "Wav2" in file_path:
            w2v2_file_path = file_path
    
    w2v2_df = pd.read_csv(w2v2_file_path)
    fw2_df = pd.read_csv(fw2_file_path)

    return(w2v2_df, fw2_df)

def reformat_dfs(w2v2_df, fw2_df, output_dir):
    w2v2_df_reformatted = fw2_df.merge(w2v2_df, on=['id', 'prompt', 'reference'], how='inner', suffixes=('', '_fw2'))

    w2v2_df_reformatted = w2v2_df_reformatted.drop_duplicates()
    fw2_df_reformatted = fw2_df.drop_duplicates()

    w2v2_df_reformatted = add_conf_mat_col_w2v2(w2v2_df_reformatted)
    w2v2_df_reformatted.to_csv('CHORECREFORMAT_Wav2Vec2.0-CGN_judgements.csv', index=False)

    fw2_df_reformatted = add_conf_mat_col_fw2(fw2_df_reformatted)
    fw2_df_reformatted.to_csv('CHORECREFORMAT_Whisper--Large-V2_judgements.csv', index=False)


def add_conf_mat_col_w2v2(df):
    filled_df = pd.DataFrame(columns=['prompt','hypothesis','prompt_aligned','prompt_aligned_rev',
                                   'hypothesis_rev','reference','prompts_plus_orth', 'prompts_plus_hypo',
                                   'id', "conf_mat_val"])
    row_number_in_file = 0
    for index, row in df.iterrows():
        row_number_in_file = row_number_in_file +1
        prompt_val = row['prompt']
        hypothesis_val = row["hypothesis_fw2"]
        prompt_aligned_val = row["prompt_aligned_fw2"]
        prompt_aligned_rev_val = row["prompt_aligned_rev_fw2"]
        hypothesis_rev_val = row["hypothesis_rev_fw2"] 
        assessor_val = row['reference']
        id_val = row["id"]
        prompts_plus_orth_val = row["prompts_plus_orth_fw2"]
        prompts_plus_hypo_val = row["prompts_plus_hypo_fw2"]
    


        conf_mat_val = calculate_conf_mat_val(prompts_plus_orth_val, prompts_plus_hypo_val)

        row_arr = [prompt_val, hypothesis_val, prompt_aligned_val, prompt_aligned_rev_val, hypothesis_rev_val, assessor_val,
                   prompts_plus_orth_val, prompts_plus_hypo_val, id_val, conf_mat_val]   
        
        filled_df.loc[row_number_in_file] = row_arr

    return filled_df

def add_conf_mat_col_fw2(df):
    filled_df = pd.DataFrame(columns=['prompt','hypothesis','prompt_aligned','prompt_aligned_rev',
                                   'hypothesis_rev','reference','prompts_plus_orth', 'prompts_plus_hypo',
                                   'id', "conf_mat_val"])
    row_number_in_file = 0
    for index, row in df.iterrows():
        row_number_in_file = row_number_in_file +1
        prompt_val = row['prompt']
        hypothesis_val = row["hypothesis"]
        prompt_aligned_val = row["prompt_aligned"]
        prompt_aligned_rev_val = row["prompt_aligned_rev"]
        hypothesis_rev_val = row["hypothesis_rev"] 
        assessor_val = row['reference']
        id_val = row["id"]
        prompts_plus_orth_val = row["prompts_plus_orth"]
        prompts_plus_hypo_val = row["prompts_plus_hypo"]
    


        conf_mat_val = calculate_conf_mat_val(prompts_plus_orth_val, prompts_plus_hypo_val)

        row_arr = [prompt_val, hypothesis_val, prompt_aligned_val, prompt_aligned_rev_val, hypothesis_rev_val, assessor_val,
                   prompts_plus_orth_val, prompts_plus_hypo_val, id_val, conf_mat_val]   
        
        filled_df.loc[row_number_in_file] = row_arr

    return filled_df


def calculate_conf_mat_val(assessor_judgement, asr_judgement):
    if assessor_judgement == 1 and asr_judgement == 1:
        return "TP"
    elif assessor_judgement == 1 and asr_judgement == 0:
        return "FN"
    elif assessor_judgement == 0 and asr_judgement == 0:
        return "TN"
    elif assessor_judgement == 0 and asr_judgement == 1:
        return "FP"

main()




