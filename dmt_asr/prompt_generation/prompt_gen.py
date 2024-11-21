import pandas as pd
import re
from itertools import product

# Function to generate variations based on the plosive voice rule
def generate_plosive_voice_variations(prompt_variations_df, prompt):
    voicedness_pairs = {
        "p": "b",
        "b": "p",
        "t": "d",
        "d": "t",
        "g": "k",
        "k": "g",
    }

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
        changes = sum(1 for original, new in zip(prompt, combination) if original != new)
        variations.append((prompt, variation, changes, 0)) 

    print(variations) 

    # Create a DataFrame with the new variations
    new_variations_df = pd.DataFrame(variations, columns=["prompt", "variation", "plosive_voice", "long/short_vowel"])
    return new_variations_df

def generate_long_short_vowel_variations(prompt_variations_df):
    # Vowel transformations for short <-> long vowels
    # vowel_pairs = {
    #     "aa": "a", "a": "aa", 
    #     "ee": "e", "e": "ee", 
    #     "oo": "o", "o": "oo", 
    #     "uu": "u", "u": "uu", 
    #     "ie": "i", "i": "ie", 
    #     "eu": "e", "e": "eu"
    # }

    vowel_pairs = {"e": ["eu", "ee"],
                   "eu": ["e"],
                   "ee": ["e"],
                   "i": ["ii", "ie"],
                   "ii": ["i"],
                   "ie": ["i"],
                   "a": ["aa"],
                   "aa": ["a"],
                   "o" : ["oo"],
                   "oo" : ["o"],
                   "u" : ["uu"],
                   "uu": ["u"]
                   }

    # Get the existing variations in the DataFrame
    existing_variations_df = prompt_variations_df.drop_duplicates()
    existing_variations = existing_variations_df["variation"].tolist()
    #print(existing_variations)

    new_variations_df = prompt_variations_df.drop_duplicates()
    new_variations = []



    # Iterate over all existing variations
    for original_variation in existing_variations:
        # print(f"\n - - - Processing variations for {original_variation} - - -")
        plosive_voice_count = prompt_variations_df[prompt_variations_df["variation"] == original_variation]["plosive_voice"].values[0]
        vowel_changes_count = prompt_variations_df[prompt_variations_df["variation"] == original_variation]["long/short_vowel"].values[0]

        for vowel, replacements in vowel_pairs.items():
            #print(f"\nVOWEL value: {vowel}\n replacement values: {replacements}\n")
            
            if vowel in original_variation:
                #print(f"\n---HIT---\n\tVowel {vowel} found in {original_variation} and replacable by {replacements}")
                
                if vowel == "e":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)
                
                if vowel == "ee" or vowel == "eu":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)

                if vowel == "i":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)
                
                if vowel == "ie" or vowel == "ii":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)
                
                if vowel == "a":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)

                if vowel == "aa":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)

                if vowel == "u":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)

                if vowel == "uu":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)

                if vowel == "o":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)

                if vowel == "oo":
                    variations = []
                    for replacement in replacements:
                        # Check if "e" is not surrounded by other vowels (i.e., only replace if it's isolated or at the edge)
                        pattern = r'(?<![aeiou])' + re.escape(vowel) + r'(?![aeiou])'
                        if re.search(pattern, original_variation):
                            modified_variation = re.sub(pattern, replacement, original_variation)
                            variations.append(modified_variation)
                    new_variations.append(variations)

        variations_list = [item for sublist in new_variations for item in sublist]
        variations_list = [item for item in variations_list if item.strip() != '']
        # print(f"---\n\tVariations of {original_variation}\t: {variations_list}\n---")

        new_row_index = len(new_variations_df)
        for item in variations_list:
            new_row = {
                'prompt': original_variation,
                'variation': item,
                'plosive_voice': plosive_voice_count,
                'long/short_vowel': 1
                }
            new_variations_df.loc[new_row_index] = new_row
            new_row_index = new_row_index+1
            

   
    return new_variations_df

# Many comments to illustrate
def generate_g_ch_variations(prompt_variations_df):
    # Mapping for g and ch replacements
    g_ch_pairs = {
        "g": "ch",
        "ch": "g"
    }

    # Add a new column for g/ch_confusion and initialize with 0
    prompt_variations_df["g/ch_confusion"] = 0

    # Create a list to store all new rows (including existing ones)
    all_rows = prompt_variations_df.to_dict("records")

    # Process each row in the DataFrame
    for row in prompt_variations_df.to_dict("records"):
        prompt = row["variation"]
        options = []
        
        # Generate replacement options for each character
        i = 0
        while i < len(prompt):
            if prompt[i:i+2] in g_ch_pairs:  # Handle "ch" as a two-character unit
                options.append([prompt[i:i+2], g_ch_pairs[prompt[i:i+2]]])
                i += 2  # Skip the next character since "ch" is two characters
            elif prompt[i] in g_ch_pairs:  # Handle "g" as a single character
                options.append([prompt[i], g_ch_pairs[prompt[i]]])
                i += 1
            else:  # No substitution needed
                options.append([prompt[i]])
                i += 1

        # Generate all combinations of replacements
        for combination in product(*options):
            variation = ''.join(combination)
            changes = sum(1 for original, new in zip(prompt, variation) if original != new)

            # If it's a new variation, add it to the rows
            if variation != prompt:
                new_row = row.copy()
                new_row["variation"] = variation
                new_row["g/ch_confusion"] = changes
                all_rows.append(new_row)

    # Create a new DataFrame with the updated rows
    updated_variations_df = pd.DataFrame(all_rows)


    #print(updated_variations_df)

    return updated_variations_df

    
    

    


def generate_prompt_variations(prompt):
    # Create a base DataFrame with just the prompt, apart from plosive_voice and long/short_vowel, all columns are created in-function
    prompt_variations_df = pd.DataFrame({
        "prompt": [prompt],
        "variation": [prompt],
        "plosive_voice": [0],
        "long/short_vowel": [0],
    })
    
    # Generate plosive voice variations and append them
    plosive_voice_variations_df = generate_plosive_voice_variations(prompt_variations_df, prompt)
    prompt_variations_df = pd.concat([prompt_variations_df, plosive_voice_variations_df], ignore_index=True)

    # Generate long/short vowel variations and append them
    long_short_vowel_variations_df = generate_long_short_vowel_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, long_short_vowel_variations_df], ignore_index=True)

    # Generate g/ch contrast variations and append them
    g_ch_confusion_df = generate_g_ch_variations(prompt_variations_df)
    prompt_variations_df = pd.concat([prompt_variations_df, g_ch_confusion_df], ignore_index=True)

    return prompt_variations_df

# Example usage
prompt = "opag"
prompt_variations_df = generate_prompt_variations(prompt)
prompt_variations_df["prompt"] = prompt

# Remove duplicates
#prompt_variations_df = prompt_variations_df.drop_duplicates()
prompt_variations_df.drop_duplicates(subset=['prompt', 'variation'], inplace=True)

print(prompt_variations_df)
