
import tgt
import pandas as pd


def lambda_fn(f) -> str:
    print(f)
    return f

def use_text_grids(tgt_file_name, word_list_id: str, participant_id: str):
    # print(tgt_file_name)
    # tg_file = get_file_path(tgt_file_name)
    tg_file = tgt_file_name

    # Read TextGrid file
    tg = tgt.io.read_textgrid(tg_file, encoding='utf-8', include_empty_intervals=False)

    # Convert TextGrid file to Formatted Table (= df with one interval on each row)
    table = tgt.io.export_to_table(tg, separator=',')
    formatted_table = [x.split(',') for x in table.split('\n')]

    tg_df = pd.DataFrame(formatted_table[1:], columns = formatted_table[0])

    tg_df_prompts = tg_df[tg_df['tier_name'] == 'Prompt']
    if tg_df_prompts.empty:
        tg_df_prompts = tg_df[tg_df['tier_name'] == 'Prompts']



    tg_df_ort_mau = tg_df[tg_df['tier_name'] == 'ORT-MAU']
    tg_df_prompts['reading_errs'] = None
    tg_df_prompts['word_list_id'] = word_list_id
    tg_df_prompts['participant_id'] = participant_id
    print(f"------------------------\n\t TG_DF_PROMPTS FOR {participant_id}\n{tg_df_prompts}------------------------")


    # for index, prompt_row in tg_df_prompts.iterrows():
    #     for _, error_row in tg_df_reading_errs.iterrows():
    #         if prompt_row['start_time'] == error_row['start_time']:
    #             tg_df_prompts.at[index, 'reading_errs'] = error_row['text']
    #             break  # Break inner loop when matched

    # start_time = 29.57
    # end_time = 30.88
    # pin starts at start_time, ends at end_time (tier 4, Prompt)
    # between start_time and end_time, 
    # find all words inside tier 1 (ort-mau) and add them to a column that matches the time of start_time

    for index, prompt_row in tg_df_prompts.iterrows():
        start_time = float(prompt_row['start_time'])
        end_time = float(prompt_row['end_time'])
        values = []
        for _, ort_mau_row in tg_df_ort_mau.iterrows():
            ort_mau_start_time = float(ort_mau_row['start_time'])
            ort_mau_end_time = float(ort_mau_row['end_time'])
            ort_mau_text = ort_mau_row['text']
            if ort_mau_start_time >= start_time and ort_mau_end_time <= end_time:
                values.append(ort_mau_text)
        values_repr = str.join(" ", values)
        tg_df_prompts.at[index, 'reading_errs'] = values_repr

    tgt_df_repr = tg_df_prompts.reset_index()
    print(f"------------------------\n\INITIAL TGT_DF_REPR FOR {participant_id}\n{tgt_df_repr}------------------------")


    tgt_df_repr = tgt_df_repr.drop(columns=['index', 'tier_type', 'tier_name', 'start_time', 'end_time'])
    tgt_df_repr = tgt_df_repr.rename(columns={"reading_errs": "orthography", "text": "prompt"})
    tgt_df_repr = tgt_df_repr.loc[:,['participant_id','word_list_id','prompt', 'orthography']]

    print(f"------------------------\n\tFINAL TGT_DF_REPR FOR {participant_id}\n{tgt_df_repr}------------------------")

    return tgt_df_repr
