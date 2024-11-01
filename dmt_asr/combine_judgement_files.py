import pandas as pd

def combine_judgement_files(df_filepaths: list[str]):
    combined_judgements_df = pd.DataFrame()

    for file_path in df_filepaths:
        curr_df = pd.read_csv(file_path)
        combined_judgements_df = pd.concat([combined_judgements_df, curr_df])

    return combined_judgements_df

def export_combined_judgement_df(combined_judgements_df, combined_judgements_filepath: str):
    combined_judgements_df.to_csv(combined_judgements_filepath, index=False)