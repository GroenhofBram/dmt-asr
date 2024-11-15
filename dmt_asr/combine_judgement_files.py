import pandas as pd

def combine_judgement_files(df_filepaths: list[str]):
    combined_judgements_df = pd.DataFrame()

    for file_path in df_filepaths:
        curr_df = pd.read_csv(file_path)
        combined_judgements_df = pd.concat([combined_judgements_df, curr_df])

    
    grouped = combined_judgements_df.groupby('id')
    result_df = pd.DataFrame()

    for id_val, group in grouped:
        # Retrieve the long string from the first row's 'hypothesis_rev'
        long_string = group.iloc[0]['hypothesis_rev']
        group = group.copy()
        
        # Check if `prompt` is in the long string and update the columns
        def update_hypothesis(x):
            if isinstance(x, str) and x in long_string:
                return x
            filtered = group.loc[group['prompt'] == x, 'hypothesis']
            return filtered.iloc[0] if not filtered.empty else "***"  # Default value if no match is found

        def update_hypothesis_rev(x):
            if isinstance(x, str) and x in long_string:
                return x
            filtered = group.loc[group['prompt'] == x, 'hypothesis_rev']
            return filtered.iloc[0] if not filtered.empty else "***"  # Default value if no match is found

        group['hypothesis'] = group['prompt'].apply(update_hypothesis)
        group['hypothesis_rev'] = group['prompt'].apply(update_hypothesis_rev)
        
        # Append the processed group
        result_df = pd.concat([result_df, group], ignore_index=True)

    # Return or print the final DataFrame
    return result_df

def export_combined_judgement_df(combined_judgements_df, combined_judgements_filepath: str):
    combined_judgements_df.to_csv(combined_judgements_filepath, index=False)