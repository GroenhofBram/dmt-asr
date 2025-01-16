import pandas as pd
import re
from itertools import product
import time

def main():
    # Can always read in prompts, but this was quick and dirty (time constraints)
    # "klas", "mooi", "koe", "arm", "groei", "strand", "bed", "eerst", "voor", "draai",
    #     "sjaal", "herfst", "duur", "straat", "leeuw", "clown", "hoek", "krant", "hout", "vriend",
    #     "gauw", "chips", "groen", "feest", "reis", "jas", "huis", "paard", "vijf", "muts", "nieuw",
    #     "kind", "bang", "oog", "zacht", "schoen", "plas", "neus", "knoop", "plank", "water", "mevrouw",
    #     "drogen", "winkel", "auto", "schouder", "verhaal", "koning", "moeilijk", "speelplaats", "drinken",
    #     "hoofdpijn", "regen", "vliegtuig", "stoppen", "opnieuw", "gooien", "schreeuwen", "moeder", "liedje",
    #     "potlood", "fietsbel", "vinger", "dichtbij", "meisje", "chauffeur", "muziek", "waarom", "scheuren",
    #     "lawaai", "zwemmen", "vuurwerk", "appel", "cola", "kussen", "eerste", "circus", "kleuren", "voetbal","poppenwagen", "konijnenhok", "elastiekje", "ruziemaken", "teddybeer", "dierentuin",
    #    "paddenstoelen", "verstoppetje", "wasmachine", "fototoestel", "toiletpapier", "vrachtwagen", "buurmannen",
    #    "vogelkooi", "olifant", "schommelen", "iedereen",
    #     "vlinder", "omdraaien",

    #prompt_list = ["ranarnararr"] 
    prompt_list = ["schoenenwinkel", "knutselen", "ophangen", "verjaardag",
        "sprookjesboek", "tandenborstel", "lucifer", "slaapkamer", "achterdeur", "ziekenhuis", "nieuwsgierig", "afblijven",
        "kabouter", "washandje", "sneeuwwitje", "goeiendag", "vakantie", "limonade", "autorijden", "eindelijk", "familie",
        "chocolade"
    ]
    total_prompts = len(prompt_list)
    for idx, prompt in enumerate(prompt_list, start=1):
        
        print(f"==============================================================================================================\n\tCurrently processing prompt '{prompt}'. This is prompt {idx} out of {total_prompts}.\n==============================================================================================================")
        prompt_variations_df = generate_prompt_variations(prompt)
        prompt_variations_df["prompt"] = prompt
        prompt_variations_df = prompt_variations_df.fillna(False)
        prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)
        filename = f"variations_{prompt}.csv"
        prompt_variations_df.to_csv(filename, index=False)

def generate_plosive_voice_variations(prompt_variations_df, prompt):
    print("Executing\t: generate_plosive_voice_variations...")
    voicedness_pairs = {
        "p": "b",
        "b": "p",
        "t": "d",
        "d": "t",
        "g": "k",
        "k": "g",
    }
    prompt_variations_df["plosive_voice"] = False

    options = []
    for char in prompt:
        if char in voicedness_pairs:
            options.append([char, voicedness_pairs[char]])
        else:
            options.append([char])
    
    # Generate all combinations of options
    variations = []
    for combination in product(*options):
        variation = ''.join(combination)
        variations.append((prompt, variation, True)) 

    new_variations_df = pd.DataFrame(variations, columns=["prompt", "variation", "plosive_voice"])
    return new_variations_df

def generate_long_short_vowel_variations(prompt_variations_df):
    print("Executing\t: generate_long_short_vowel_variations...")

    # Define vowel transformations
    vowel_pairs = {
        "e": ["eu", "ee"], "eu": ["e"], "ee": ["e"],
        "i": ["ii", "ie"], "ii": ["i"], "ie": ["i"],
        "a": ["aa"], "aa": ["a"],
        "o": ["oo"], "oo": ["o"],
        "u": ["uu"], "uu": ["u"]
    }

    # Ensure the 'long_short_vowel' column exists
    if "long_short_vowel" not in prompt_variations_df.columns:
        prompt_variations_df["long_short_vowel"] = False

    # List to hold new variations
    new_rows = []

    # Iterate over each existing variation
    for _, row in prompt_variations_df.iterrows():
        original_variation = row["variation"]

        # Apply transformations for each vowel and its replacements
        for vowel, replacements in vowel_pairs.items():
            # Use regex to match isolated vowels (not surrounded by other vowels)
            pattern = rf"(?<![aeiou]){re.escape(vowel)}(?![aeiou])"

            if re.search(pattern, original_variation):  # Check if the vowel exists in the string
                for replacement in replacements:
                    # Create the new variation
                    modified_variation = re.sub(pattern, replacement, original_variation)

                    # Skip duplicates
                    if modified_variation != original_variation and not (
                        (prompt_variations_df["variation"] == modified_variation).any() or
                        any(new_row["variation"] == modified_variation for new_row in new_rows)
                    ):
                        # Create a new row with updated variation
                        new_row = row.copy()
                        new_row["variation"] = modified_variation
                        new_row["long_short_vowel"] = True
                        new_rows.append(new_row)

    # Create a DataFrame for the new rows
    new_variations_df = pd.DataFrame(new_rows)

    # Combine the original DataFrame with the new variations
    result_df = pd.concat([prompt_variations_df, new_variations_df], ignore_index=True)

    return result_df

def generate_g_ch_variations(prompt_variations_df):
    
    # Mapping for g and ch replacements (including deletion as "")
    print("Executing\t: generate_g_ch_variations...")    
    g_ch_pairs = {
        "sch": ["sh", "sg", "s"],  
        "sh": ["sch", "ch", "sj", "s"],
        "ch": ["g", "sh"],
        "g": ["ch"],
    }

    # Add a new column for g/ch_confusion and initialize with False
    prompt_variations_df["g/ch_confusion"] = False

    # Create a list to store all new rows (including existing ones)
    all_rows = prompt_variations_df.to_dict("records")

    # Process each row in the DataFrame
    for row in prompt_variations_df.to_dict("records"):
        prompt = row["variation"]
        options = []

        # Generate replacement options for each character or substring
        i = 0
        while i < len(prompt):
            # Check for multi-character matches first (e.g., "sch", "ch")
            match_found = False
            for pattern in sorted(g_ch_pairs.keys(), key=len, reverse=True):  # Check longer patterns first
                if prompt[i:i+len(pattern)] == pattern:
                    options.append([pattern] + g_ch_pairs[pattern])  # Original + replacements
                    i += len(pattern)
                    match_found = True
                    break
            
            if not match_found:  # Single-character handling
                options.append([prompt[i]])
                i += 1

        # Generate all combinations of replacements
        for combination in product(*options):
            variation = ''.join(combination)

            # If it's a new variation, add it to the rows
            if variation != prompt:
                new_row = row.copy()
                new_row["variation"] = variation
                new_row["g/ch_confusion"] = True  # Set confusion flag
                all_rows.append(new_row)

    # Create a new DataFrame with the updated rows
    updated_variations_df = pd.DataFrame(all_rows)

    return updated_variations_df

def generate_oe_oo_variations(prompt_variations_df):
    print("Executing\t: generate_oe_oo_variations...")    
    prompt_variations_df["oe/oo_substitution"] = False
    vowel_pairs = {"oe": ["oo"],
                   "oo": ["oe"],
    }

    # Get the existing variations in the DataFrame
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()

    new_variations_df = prompt_variations_df.drop_duplicates()
    new_variations = []

    # Iterate over all existing variations
    for original_variation in existing_variations:
        for vowel, replacements in vowel_pairs.items():
            if vowel in original_variation:
                variations = []
                for replacement in replacements:
                    pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                    if re.search(pattern, original_variation):
                        modified_variation = re.sub(pattern, replacement, original_variation)
                        variations.append(modified_variation)
                new_variations.append(variations)

        variations_list = [item for sublist in new_variations for item in sublist]
        variations_list = [item for item in variations_list if item.strip() != '']

        new_row_index = len(new_variations_df)
        for item in variations_list:
            # Retrieve the original row from the DataFrame
            original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()

            # Check if the variation involves 'oe/oo' substitution
            original_row["oe/oo_substitution"] = True

            # Update the variation column with the new variation
            original_row["variation"] = item

            # Add the new row to the DataFrame
            new_variations_df = pd.concat([new_variations_df, original_row], ignore_index=True)
            
            new_row_index += 1

    return new_variations_df

def generate_double_single_consonant_variations(prompt_variations_df):
    print("Executing\t: generate_double_single_consonant_variations...") 
    prompt_variations_df["double_single_consonant_substitution"] = False
    consonant_pairs = {
        "b": ["bb", "b"],
        "c": ["cc", "c"],
        "d": ["dd", "d"],
        "f": ["ff", "f"],
        "g": ["gg", "g"],
        "h": ["hh", "h"],
        "j": ["jj", "j"],
        "k": ["kk", "k"],
        "l": ["ll", "l"],
        "m": ["mm", "m"],
        "n": ["nn", "n"],
        "p": ["pp", "p"],
        "q": ["qq", "q"],
        "r": ["rr", "r"],
        "s": ["ss", "s"],
        "t": ["tt", "t"],
        "v": ["vv", "v"],
        "w": ["ww", "w"],
        "x": ["xx", "x"],
        "z": ["zz", "z"],
    }

    # Get the existing variations in the DataFrame
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()

    new_variations_df = prompt_variations_df.drop_duplicates()

    # Iterate over all existing variations
    for original_variation in existing_variations:
        new_variations = []

        for consonant, replacements in consonant_pairs.items():
            # Regex to ensure consonant is not surrounded by itself
            pattern = r'(?<!' + re.escape(consonant) + r')' + re.escape(consonant) + r'(?!' + re.escape(consonant) + r')'

            # Doubling: replace consonant with its doubled form
            doubled_variation = re.sub(pattern, replacements[0], original_variation)
            new_variations.append(doubled_variation)

            # Singling: replace doubled consonant with its single form
            doubled_pattern = r'(?<!' + re.escape(consonant) + r')' + re.escape(replacements[0]) + r'(?!' + re.escape(consonant) + r')'
            singled_variation = re.sub(doubled_pattern, consonant, original_variation)
            new_variations.append(singled_variation)

        # Remove empty or duplicate variations
        new_variations = list(set(new_variations))  # Removing duplicates
        new_variations = [variation for variation in new_variations if variation.strip() != '']

        # Create new rows with the generated variations
        for item in new_variations:
            original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()

            # Mark that this row involves consonant substitution
            original_row["double_single_consonant_substitution"] = True

            # Update the variation column with the new variation
            original_row["variation"] = item

            # Add the new row to the DataFrame
            new_variations_df = pd.concat([new_variations_df, original_row], ignore_index=True)

    return new_variations_df

def generate_k_c_variations(prompt_variations_df):
    print("Executing\t: generate_k_c_variations...") 
    prompt_variations_df["k/c_substitution"] = False
    consonant_pairs = {
        "c": ["k"],
        "k": ["c"],
    }

    # Get the existing variations in the DataFrame
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()

    new_variations_df = prompt_variations_df.drop_duplicates()

    # Iterate over all existing variations
    for original_variation in existing_variations:
        new_variations = []

        for consonant, replacements in consonant_pairs.items():
            # Change consonant to its replacement
            for replacement in replacements:
                # Replace the consonant in the original variation
                variation = original_variation.replace(consonant, replacement)
                new_variations.append(variation)

        # Remove empty or duplicate variations
        new_variations = list(set(new_variations))  # Removing duplicates
        new_variations = [variation for variation in new_variations if variation.strip() != '']

        # Create new rows with the generated variations
        for item in new_variations:
            original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()

            # Mark that this row involves k/c substitution
            original_row["k/c_substitution"] = True

            # Update the variation column with the new variation
            original_row["variation"] = item

            # Add the new row to the DataFrame
            new_variations_df = pd.concat([new_variations_df, original_row], ignore_index=True)

    return new_variations_df

def generate_au_ou_variations(prompt_variations_df):
    print("Executing\t: generate_au_ou_variations...") 
    prompt_variations_df["au/ou_substitution"] = False
    vowel_pairs = {"au": ["ou"],
                   "ou": ["au"],
    }

    # Get the existing variations in the DataFrame
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()

    new_variations_df = prompt_variations_df.drop_duplicates()
    new_variations = []

    # Iterate over all existing variations
    for original_variation in existing_variations:
        for vowel, replacements in vowel_pairs.items():
            if vowel in original_variation:
                variations = []
                for replacement in replacements:
                    pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                    if re.search(pattern, original_variation):
                        modified_variation = re.sub(pattern, replacement, original_variation)
                        variations.append(modified_variation)
                new_variations.append(variations)

        variations_list = [item for sublist in new_variations for item in sublist]
        variations_list = [item for item in variations_list if item.strip() != '']

        new_row_index = len(new_variations_df)
        for item in variations_list:
            # Retrieve the original row from the DataFrame
            original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()

            # Check if the variation involves 'oe/oo' substitution
            original_row["ou/au_substitution"] = True

            # Update the variation column with the new variation
            original_row["variation"] = item

            # Add the new row to the DataFrame
            new_variations_df = pd.concat([new_variations_df, original_row], ignore_index=True)
            
            new_row_index += 1

    return new_variations_df

def generate_ei_ij_variations(prompt_variations_df):
    print("Executing\t: generate_ei_ij_variations...") 
    prompt_variations_df["ei/ij_substitution"] = False
    vowel_pairs = {"ei": ["ij"],
                   "ij": ["ei"],
    }

    # Get the existing variations in the DataFrame
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()

    new_variations_df = prompt_variations_df.drop_duplicates()
    new_variations = []

    # Iterate over all existing variations
    for original_variation in existing_variations:
        for vowel, replacements in vowel_pairs.items():
            if vowel in original_variation:
                variations = []
                for replacement in replacements:
                    pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                    if re.search(pattern, original_variation):
                        modified_variation = re.sub(pattern, replacement, original_variation)
                        variations.append(modified_variation)
                new_variations.append(variations)

        variations_list = [item for sublist in new_variations for item in sublist]
        variations_list = [item for item in variations_list if item.strip() != '']

        new_row_index = len(new_variations_df)
        for item in variations_list:
            # Retrieve the original row from the DataFrame
            original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()

            # Check if the variation involves 'oe/oo' substitution
            original_row["ei/ij_substitution"] = True

            # Update the variation column with the new variation
            original_row["variation"] = item

            # Add the new row to the DataFrame
            new_variations_df = pd.concat([new_variations_df, original_row], ignore_index=True)
            
            new_row_index += 1

    return new_variations_df

def generate_fricative_voice_variations(prompt_variations_df):
    print("Executing\t: generate_fricative_voice_variations...") 
    prompt_variations_df["fricative_voice"] = False
    consonant_pairs = {
        "f": ["v"],
        "v": ["f"],
        "s": ["z"],
        "z": ["s"]
    }

    # Get the existing variations in the DataFrame
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()

    new_variations_df = prompt_variations_df.drop_duplicates()

    # Iterate over all existing variations
    for original_variation in existing_variations:
        new_variations = []

        # Apply each consonant pair substitution
        for consonant, replacements in consonant_pairs.items():
            # Replace the consonant in the original variation
            for replacement in replacements:
                variation = original_variation.replace(consonant, replacement)
                new_variations.append(variation)

        # Remove empty or duplicate variations
        new_variations = list(set(new_variations))  # Removing duplicates
        new_variations = [variation for variation in new_variations if variation.strip() != '']

        # Create new rows with the generated variations
        for item in new_variations:
            original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()

            # Mark that this row involves fricative voicing substitution
            original_row["fricative_voice"] = True

            # Update the variation column with the new variation
            original_row["variation"] = item

            # Add the new row to the DataFrame
            new_variations_df = pd.concat([new_variations_df, original_row], ignore_index=True)

    return new_variations_df

def generate_i_y_variations(prompt_variations_df):
    print("Executing\t: generate_i_y_variations...") 
    prompt_variations_df["i/y_substitution"] = False
    vowel_pairs = {"i": ["y"],
                   "y": ["i"],
    }

    # Get the existing variations in the DataFrame
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()

    new_variations_df = prompt_variations_df.drop_duplicates()
    new_variations = []

    # Iterate over all existing variations
    for original_variation in existing_variations:
        for vowel, replacements in vowel_pairs.items():
            if vowel in original_variation:
                variations = []
                for replacement in replacements:
                    pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                    if re.search(pattern, original_variation):
                        modified_variation = re.sub(pattern, replacement, original_variation)
                        variations.append(modified_variation)
                new_variations.append(variations)

        variations_list = [item for sublist in new_variations for item in sublist]
        variations_list = [item for item in variations_list if item.strip() != '']

        new_row_index = len(new_variations_df)
        for item in variations_list:
            # Retrieve the original row from the DataFrame
            original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()

            # Check if the variation involves 'oe/oo' substitution
            original_row["i/y_substitution"] = True

            # Update the variation column with the new variation
            original_row["variation"] = item

            # Add the new row to the DataFrame
            new_variations_df = pd.concat([new_variations_df, original_row], ignore_index=True)
            
            new_row_index += 1

    return new_variations_df

def generate_liquid_variations(prompt_variations_df):
    print("Executing\t: generate_liquid_variations...") 
    # Mapping for liquid substitutions and deletions
    liquid_pairs = {
        "l": ["ll", "r", "rr", ""],  
        "ll": ["l", "r", "rr", ""],  
        "r": ["rr", "l", "ll", ""],  
        "rr": ["r", "l", "ll", ""]   
    }

    # Add a new column for liquid_deletion and initialize with False
    prompt_variations_df["liquid_substitution_change"] = False

    # Create a list to store all new rows (including existing ones)
    all_rows = prompt_variations_df.to_dict("records")

    # Process each row in the DataFrame
    for row in prompt_variations_df.to_dict("records"):
        prompt = row["variation"]
        options = []

        # Generate replacement options for each character or substring
        i = 0
        while i < len(prompt):
            # Check for multi-character matches first (e.g., "ll", "rr")
            match_found = False
            for pattern in sorted(liquid_pairs.keys(), key=len, reverse=True):  # Check longer patterns first
                if prompt[i:i+len(pattern)] == pattern:
                    options.append([pattern] + liquid_pairs[pattern])  # Original + replacements
                    i += len(pattern)
                    match_found = True
                    break
            
            if not match_found:  # Single-character handling (if no multi-character match)
                options.append([prompt[i]])
                i += 1

        # Generate all combinations of replacements
        for combination in product(*options):
            variation = ''.join(combination)

            # If it's a new variation, add it to the rows
            if variation != prompt:
                new_row = row.copy()
                new_row["variation"] = variation
                new_row["liquid_substitution_change"] = True  
                all_rows.append(new_row)

    # Create a new DataFrame with the updated rows
    updated_variations_df = pd.DataFrame(all_rows)

    return updated_variations_df

def generate_nasal_variations(prompt_variations_df):
    print("Executing\t: generate_nasal_variations...")

    # Nasal substitutions mapping
    nasal_pairs = {
        "n": ["nn", "m", "mm", "ng"],
        "nn": ["n", "m", "mm", "ng"],
        "m": ["n", "nn", "mm", "ng"],
        "mm": ["n", "nn", "m", "ng"],
        "ng": ["n", "nn", "m", "mm"],
    }

    # Add a new column for nasal_substitution flag
    prompt_variations_df["nasal_substitution"] = False

    # Create a set to track generated variations and prevent duplicates
    generated_variations = set(prompt_variations_df["variation"].tolist())

    # Create a list to store all new rows (including existing ones)
    all_rows = prompt_variations_df.to_dict("records")

    # Function to check if a nasal is surrounded by another nasal or followed by 'g'
    def can_substitute(prompt, i, nasal):
        # Look ahead 1 character and 1 character before
        if i + len(nasal) < len(prompt):
            if prompt[i-1:i] in ['n', 'm', 'ng', 'nn', 'mm', "g"]:  # Check for surrounding nasals/g
                return False
        return True

    # Set maximum variation limit
    variation_limit = 399999999999000000

    # To track the number of new variations generated in each round
    no_new_variations_count = 0
    max_no_new_variations = 39900  # Max attempts without finding new variations

    # Process each row in the DataFrame
    for row in prompt_variations_df.to_dict("records"):
        prompt = row["variation"]
        options = []

        # Generate replacement options for each character or substring
        i = 0
        while i < len(prompt):
            match_found = False
            # Try matching each nasal substitution pair
            for nasal in nasal_pairs.keys():
                if prompt[i:i+len(nasal)] == nasal and can_substitute(prompt, i, nasal):
                    options.append([nasal] + nasal_pairs[nasal])  # Original nasal + possible replacements
                    i += len(nasal)
                    match_found = True
                    break

            if not match_found:  # If no nasal found, just append the character
                options.append([prompt[i]])
                i += 1

        # Generate all combinations of replacements
        new_variations = []
        for combination in product(*options):
            variation = ''.join(combination)

            # If it's a new variation, add it to the rows
            if variation != prompt and variation not in generated_variations:
                new_row = row.copy()
                new_row["variation"] = variation
                new_row["nasal_substitution"] = True  # Set nasal substitution flag
                new_variations.append(new_row)
                generated_variations.add(variation)

        # If new variations were added, update the all_rows list
        if new_variations:
            all_rows.extend(new_variations)
            no_new_variations_count = 0  # Reset counter if new variations are found
        else:
            no_new_variations_count += 1  # Increment counter if no new variations

        # Stop if we've reached the variation limit or plateaued
        if len(generated_variations) >= variation_limit or no_new_variations_count >= max_no_new_variations:
            break

    # Create a new DataFrame with the updated rows
    updated_variations_df = pd.DataFrame(all_rows)

    return updated_variations_df

def generate_final_deletion_variations(prompt_variations_df):
    print("Executing\t: generate_final_deletion_variations...")

    # Ensure unique rows and initialize the 'final_deletion' column to False
    prompt_variations_df = prompt_variations_df.copy()
    if "final_deletion" not in prompt_variations_df.columns:
        prompt_variations_df["final_deletion"] = False

    # Collect new variations
    new_rows = []
    generated_variations = set(prompt_variations_df["variation"].tolist())  # Track already generated variations
    variation_limit = 99999000000  # Set a maximum number of variations

    no_new_variations_count = 0
    max_no_new_variations = 30000  # Max attempts without finding new variations

    # Iterate over the variations to generate final deletion variations
    for _, row in prompt_variations_df.iterrows():
        original_variation = row["variation"]

        # Skip variations that are too short for deletion
        if len(original_variation) > 1:
            new_variation = original_variation[:-1]

            # Check if the new variation already exists
            if new_variation not in generated_variations:
                # Create a new row with the modified variation
                new_row = row.copy()
                new_row["variation"] = new_variation
                new_row["final_deletion"] = True
                new_rows.append(new_row)

                # Add to the set of generated variations
                generated_variations.add(new_variation)

            # If the number of new variations exceeds the limit, break
            if len(generated_variations) >= variation_limit:
                break

    # Create a DataFrame for the new rows
    new_variations_df = pd.DataFrame(new_rows)

    # Combine the original DataFrame with the new variations
    result_df = pd.concat([prompt_variations_df, new_variations_df], ignore_index=True)

    return result_df

def generate_n_insertion_variations(prompt_variations_df):
    prompt_variations_df["n_insertion"] = False
    
    vowels = "aeiou"  # Define vowels
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()

    new_variations_df = prompt_variations_df.drop_duplicates()

    variation_limit = 999999999999  # Set the maximum number of variations
    generated_variations = set(existing_variations)  # Set to track unique variations
    
    # To control the loop's termination and avoid infinite loops
    no_new_variations_count = 0
    max_no_new_variations = 3000  # Max attempts without finding new variations

    # Iterate over all existing variations
    for original_variation in existing_variations:
        new_variations = [original_variation]  # Start with the original variation
        
        # Track variations generated in this round
        variations_this_round = set()
        
        # Check all positions where an "n" can be inserted
        for i in range(len(original_variation)):
            if original_variation[i] in vowels:
                # We can insert an "n" before or after the vowel
                variations_to_add = []
                
                # Insert "n" before the vowel (if not already there)
                if i == 0 or original_variation[i-1] != 'n':
                    variations_to_add.append(original_variation[:i] + 'n' + original_variation[i:])
                
                # Insert "n" after the vowel (if not already there)
                if i == len(original_variation) - 1 or original_variation[i+1] != 'n':
                    variations_to_add.append(original_variation[:i+1] + 'n' + original_variation[i+1:])
                
                # Add all the new variations to the list
                new_variations.extend(variations_to_add)

        # Create all combinations of "n" insertions, if there are multiple positions
        all_combinations = []
        for variation in new_variations:
            variations_to_add = [variation]  # Initialize with the current variation
            for i in range(len(variation)):
                if variation[i] in vowels:
                    # Insert "n" before or after the vowel
                    new_variations = []
                    if i == 0 or variation[i-1] != 'n':
                        new_variations.append(variation[:i] + 'n' + variation[i:])
                    if i == len(variation) - 1 or variation[i+1] != 'n':
                        new_variations.append(variation[:i+1] + 'n' + variation[i+1:])
                    variations_to_add.extend(new_variations)
            all_combinations.extend(variations_to_add)

        # Remove duplicates and empty variations
        all_combinations = list(set(all_combinations))
        all_combinations = [variation for variation in all_combinations if variation.strip() != '']

        # Track how many new variations were generated in this round
        new_generated = 0

        # Create new rows with the generated variations
        for item in all_combinations:
            if item not in generated_variations:
                original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()

                # Mark that this row involves "n" insertion
                original_row["n_insertion"] = True

                # Update the variation column with the new variation
                original_row["variation"] = item

                # Add the new row to the DataFrame
                new_variations_df = pd.concat([new_variations_df, original_row], ignore_index=True)
                
                # Add to the set of generated variations
                generated_variations.add(item)
                variations_this_round.add(item)
                new_generated += 1

        # If no new variations were generated, count the round
        if new_generated == 0:
            no_new_variations_count += 1
        else:
            no_new_variations_count = 0

        # Stop if we've not generated new variations for several rounds
        if no_new_variations_count >= max_no_new_variations or len(new_variations_df) >= variation_limit:
            break

    return new_variations_df.head(variation_limit)

def generate_space_insertion_variations(prompt_variations_df):
    print("Executing\t: generate_space_insertion_variations...") 
    
    # Initialize a list to hold new variations
    new_rows = []
    
    # Drop duplicates early to avoid redundant processing
    existing_variations_df = prompt_variations_df.drop_duplicates(subset=["variation"])
    existing_variations = existing_variations_df["variation"].tolist()

    # Iterate over all existing variations
    for original_variation in existing_variations:
        # Generate space insertions at all possible positions, starting from position 1
        new_variations = {original_variation}  # Start with the original variation (use set to avoid duplicates)
        
        for i in range(1, len(original_variation)):  # Starting from 1 to avoid space at the start
            new_variation = original_variation[:i] + ' ' + original_variation[i:]
            new_variations.add(new_variation)

        # Remove empty variations (if any)
        new_variations = {variation for variation in new_variations if variation.strip() != ''}
        
        # Create new rows with the generated variations
        for item in new_variations:
            original_row = existing_variations_df.loc[existing_variations_df['variation'] == original_variation].copy()
            original_row["space_insertion"] = True
            original_row["variation"] = item
            
            new_rows.append(original_row)
    
    # Append all the new rows to the original DataFrame at once
    new_variations_df = pd.concat([existing_variations_df] + new_rows, ignore_index=True)
    new_variations_df['space_insertion'] = new_variations_df['space_insertion'].fillna(False)


    return new_variations_df

def generate_prompt_variations(prompt):
    start_time = time.time()
    # Create a base DataFrame with just the prompt, apart from plosive_voice and long/short_vowel, all columns are created in-function
    prompt_variations_df = pd.DataFrame({
        "prompt": [prompt],
        "variation": [prompt]
    })
    
    print(f"------------------------------------------------------------------------------------------------------------------\nCurrent Prompt: {prompt}")
    # Generate plosive voice variations and append them
    plosive_voice_variations_df = generate_plosive_voice_variations(prompt_variations_df, prompt)
    prompt_variations_df = pd.concat([prompt_variations_df, plosive_voice_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate long/short vowel variations and append them
    long_short_vowel_variations_df = generate_long_short_vowel_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, long_short_vowel_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate g/ch contrast variations and append them
    g_ch_confusion_df = generate_g_ch_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, g_ch_confusion_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate oe/oo contrast variations and append them
    oeoo_variations_df = generate_oe_oo_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, oeoo_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    au_ou_variations_df = generate_au_ou_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, au_ou_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate ei/ij contrast variations and append them
    ei_ij_variations_df = generate_ei_ij_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, ei_ij_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate double/single consonant variations and apppend them
    double_single_consonant_variations_df = generate_double_single_consonant_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, double_single_consonant_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate k/c consonant variations and apppend them
    k_c_variations_df = generate_k_c_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, k_c_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate frivative voice variations and append them
    fricative_voice_variations_df = generate_fricative_voice_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, fricative_voice_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate i/y substitutions and append them
    # i_y_variations_df = generate_i_y_variations(prompt_variations_df)
    # prompt_variations_df = pd.concat([prompt_variations_df, i_y_variations_df], ignore_index=True)
    # prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate liquid substitutions/deletions and append them
    liquid_variations_df = generate_liquid_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, liquid_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

    # Generate nasal substitutions and append them
    nasal_variations_df = generate_nasal_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, nasal_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)    

    # Generate final deletion variaitons and append them
    final_deletion_variations_df = generate_final_deletion_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, final_deletion_variations_df], ignore_index=True)
    prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True) 

    # Generate N insertion variaitons and append them
    # n_insertion_variations_df = generate_n_insertion_variations(prompt_variations_df)
    # prompt_variations_df = pd.concat([prompt_variations_df, n_insertion_variations_df], ignore_index=True)
    #prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True) 

    # #Generate space insertion variaitons and append them
    # space_insertion_variations_df = generate_space_insertion_variations(prompt_variations_df)
    # prompt_variations_df = pd.concat([prompt_variations_df, space_insertion_variations_df], ignore_index=True)
    # prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True) 

    curr_time = time.time()
    print(f"Finished generating all variations of: {prompt}\nTotal time elapsed (s): {curr_time-start_time}\n------------------------------------------------------------------------------------------------------------------")
    return prompt_variations_df


main()
