from os import makedirs
import sys
from pandas import DataFrame, Series, concat, merge
from os.path import join

import pytest
from dmt_asr.adagt.run_init import two_way_alignment
from dmt_asr.confusion_matrix import add_binaries, create_confusion_matrix, export_conf_matrix, export_df_data, get_binary_lists, read_prompt_file
import re

from dmt_asr.judgement_assessor.assessor import calculate_assessor_judgement
from dmt_asr.judgement_asr.asr_baseline import calculate_asr_baseline_judgement

def process_conf_matrix(asr_transcriptions: str, participant_audio_id: str, base_session_folder: str, ortho_df: DataFrame):
    try:
        print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
        print(f"Processing Confusion matrix for path {base_session_folder}")
        # Trim the base_session_folder to keep only the part before ' ---- '
        base_session_folder = base_session_folder.split(' ---- ')[0]
        print(f"Updated base_session_folder: {base_session_folder}")
        print("\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
        print(ortho_df)
        print(participant_audio_id)
        print(asr_transcriptions)
        print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")

        base_df_with_binaries = process_df(participant_audio_id, asr_transcriptions, ortho_df)
        base_data_dir = join(base_session_folder, "all_data")
        makedirs(base_data_dir, exist_ok=True)

        #print("HERE (LINE 25 of process_confmatrix.py)")


        csv_filename = f"{participant_audio_id}.csv"
        export_df_data(
            df=base_df_with_binaries,
            file_name=csv_filename,
            base_dir=base_data_dir,
            is_csv=True
        )

        json_filename = f"{participant_audio_id}.json"
        export_df_data(
            df=base_df_with_binaries,
            file_name=json_filename,
            base_dir=base_data_dir,
            is_csv=False
        )

        print(f"Created {base_data_dir} =====> {csv_filename}")
        ref_list_binary, hyp_list_binary = get_binary_lists(base_df_with_binaries)
        conf_matrix = create_confusion_matrix(ref_list_binary, hyp_list_binary)
        print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
        print(conf_matrix)
        print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n")
        export_conf_matrix(base_data_dir, conf_matrix)
    except Exception as e:
        print(f"Error during processing: {e}")

def get_prompt_file_name(participant_audio_id: str):
    if 'kaart1A' in participant_audio_id:
        return "kaart1A.txt"
    elif 'kaart2A' in participant_audio_id:
        return "kaart2A.txt"
    elif 'kaart3A' in participant_audio_id:
        return "kaart3A.txt"
    elif 'kaart1B' in participant_audio_id:
        return "kaart1B.txt"
    elif 'kaart2B' in participant_audio_id:
        return "kaart2B.txt"
    elif 'kaart3B' in participant_audio_id:
        return "kaart3B.txt"

def generate_df(prompts_list: list[str], asr_transcriptions: str):
    prompts = " ".join(prompts_list)
    aligned_df = two_way_alignment(prompts, asr_transcriptions.lower())
    print("\n\nADAGT\n\n")
    print(aligned_df)
    return aligned_df.reset_index().rename(columns={"index": "prompt", "aligned_asrTrans": "hypothesis", "reversed_aligned_asrTrans": "hypothesis_rev"})

def process_df(participant_audio_id: str, asr_transcriptions: str, ortho_df: DataFrame):
    try:
        prompt_file_name = get_prompt_file_name(participant_audio_id)
        prompts_list = read_prompt_file(prompt_file_name)
        print("Prompts List:", prompts_list)
        print("ASR transcription List:", asr_transcriptions)
        asr_transcriptions = re.sub(r'[^a-zA-Z\s]', '', asr_transcriptions)
        # print(f"!!!!!!!!!!!!!!!!!!!!!!!!! FIXED ASR TRANSCRIPTION !!!!!!!!!!!\n{asr_transcriptions}")


        end_df = generate_df(prompts_list, asr_transcriptions)


        print("Generated DF:", end_df)
        print("End DF columns:", end_df.columns)
        print("Ortho DF columns:", ortho_df.columns)
        
        if "orthography" not in ortho_df.columns:
            raise ValueError("Column 'orthography' not found in ortho_df")
        
        base_df = concat([end_df, ortho_df[["orthography"]]], axis=1)
        print("Base DF before dropna:", base_df)
        
        base_df = base_df.dropna()
        base_df = base_df.rename(columns={"orthography": "reference"})
        base_df_with_binaries = add_binaries(base_df)
        base_df_with_binaries = base_df_with_binaries.drop(columns=['correct'])
        base_df_with_binaries['id'] = participant_audio_id

        print("Base DF with binaries:", base_df_with_binaries)

        return base_df_with_binaries
    except Exception as e:
        print(f"Error during dataframe processing: {e}")
        return DataFrame()

def fill_assessor_judgements(combined_judgements_df):
    filled_df = DataFrame(columns=['prompt','hypothesis','prompt_aligned','prompt_aligned_rev',
                                   'hypothesis_rev','reference','prompts_plus_orth', 'prompts_plus_hypo',
                                   'id'])

    row_number_in_file = 0
    for index, row in combined_judgements_df.iterrows():
        row_number_in_file = row_number_in_file +1
        prompt_val = row['prompt']
        hypothesis_val = row["hypothesis"]
        prompt_aligned_val = row["prompt_aligned"]
        prompt_aligned_rev_val = row["prompt_aligned_rev"]
        hypothesis_rev_val = row["hypothesis_rev"] 
        assessor_val = row['reference']
        prompts_plus_hypo_val = row["prompts_plus_hypo"]
        id_val = row["id"]
        prompts_plus_orth_val = calculate_assessor_judgement(prompt_val, assessor_val)
        row_arr = [prompt_val, hypothesis_val, prompt_aligned_val, prompt_aligned_rev_val, hypothesis_rev_val, assessor_val,
                   prompts_plus_orth_val, prompts_plus_hypo_val, id_val]

        #combined_judgements_df.at[index, "prompts_plus_orth"] = judgement_val
        

        filled_df.loc[row_number_in_file] = row_arr



        # print(f"\nIndex: {index} ------\nrow: {row}\nPrompt: {prompt_val} ----- assessor: {assessor_val} ----- judgement: {prompts_plus_orth_val}")
    
    #print(f"\n\n\n\n\n\n\n OoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo\n\tDF AFTER ASSESSOR JUDGEMENTS\nOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo \n\n\n\n\n\n\n{combined_judgements_df}")

    # print(f"LEN ORIGINAL DF: {len(combined_judgements_df)} ----- LEN NEW DF: {len(filled_df)}")
    return filled_df



def fill_asr_baseline_judgements(combined_judgements_df):
    filled_df = DataFrame(columns=['prompt','hypothesis','prompt_aligned','prompt_aligned_rev',
                                   'hypothesis_rev','reference','prompts_plus_orth', 'prompts_plus_hypo',
                                   'id'])
    
    


    row_number_in_file = 0
    for index, row in combined_judgements_df.iterrows():
        row_number_in_file = row_number_in_file +1
        prompt_val = row['prompt']
        hypothesis_val = row["hypothesis"]
        prompt_aligned_val = row["prompt_aligned"]
        prompt_aligned_rev_val = row["prompt_aligned_rev"]
        hypothesis_rev_val = row["hypothesis_rev"] 
        assessor_val = row['reference']
        id_val = row["id"]
        prompts_plus_orth_val = row["prompts_plus_orth"]

        prompts_plus_hypo_val = calculate_asr_baseline_judgement(prompt_val, hypothesis_val, hypothesis_rev_val)

        row_arr = [prompt_val, hypothesis_val, prompt_aligned_val, prompt_aligned_rev_val, hypothesis_rev_val, assessor_val,
                   prompts_plus_orth_val, prompts_plus_hypo_val, id_val]   
        
        filled_df.loc[row_number_in_file] = row_arr
    




    return filled_df


def fill_agreement_metrics(combined_judgements_df):
    filled_df = DataFrame(columns=['prompt','hypothesis','prompt_aligned','prompt_aligned_rev',
                                   'hypothesis_rev','reference','prompts_plus_orth', 'prompts_plus_hypo',
                                   'id', "conf_mat_val"])
    row_number_in_file = 0
    for index, row in combined_judgements_df.iterrows():
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