import pytest
from itertools import product

@pytest.mark.unit
def calculate_assessor_judgement(prompt: str, assessor: str) -> int:
    #print(f"\n~~~~PROMPT: {prompt}\tASSESSOR: {assessor}\n TYPES:~~~~{type(assessor)} ~~~~~ {type(prompt)}\n~~~~\t~~~~")
    prompt = str(prompt)
    assessor = str(assessor)

    if prompt == assessor:
        return 0
    
    if prompt in assessor.split():
        return 0
    
    assessor_no_spaces = assessor.replace(" ", "")
    if prompt == assessor_no_spaces:
        return 0
        
    assessor_no_hyphens = assessor.replace("-", "")
    if prompt == assessor_no_hyphens:
        return 0

    # Check if prompt is found in assessor surrounded by hyphens
    if f"-{prompt}-" in assessor or assessor.startswith(f"{prompt}-") or assessor.endswith(f"-{prompt}") or assessor == prompt or f" {prompt} " in assessor or assessor.startswith(f"{prompt} ") or assessor.endswith(f" {prompt}"):
        return 0
    
    prompt_variations = generate_prompt_variations_voice(prompt)
    prompt_variations = generate_prompt_variatons_n_insertions(prompt_variations)
    if assessor_no_hyphens in prompt_variations:
        return 0
       

    else:
        return 1
    
def generate_prompt_variations_voice(voicedness_prompt):
    voicedness_pairs = {
        "p": "b",
        "b": "p",
        "t": "d",
        "d": "t",
        "f": "v",
        "v": "f",
        "g": "k",
        "k": "g",
        "z": "s",
        "s": "z"
    }

    # Set for variations
    prompt_var_options = set([voicedness_prompt])

    # For each character in the prompt, if it's in the voicedness pairs, generate alternatives
    alternatives = []
    for char in voicedness_prompt:
        if char in voicedness_pairs:
            # Create list of original char and pair
            alternatives.append([char, voicedness_pairs[char]])
        else:
            # If there's no pair, just keep the character as is
            alternatives.append([char])

    # Generate all combinations
    for variation in product(*alternatives):
        prompt_var_options.add("".join(variation))

    return prompt_var_options


def generate_prompt_variatons_n_insertions(prompt_var_options):
    vowels = "aeiou"
    new_variations = set()

    for variation in prompt_var_options:
        # List to store all positions where "n" can be inserted
        insertion_points = [(i, i + 1) for i, char in enumerate(variation) if char in vowels]
        
        # Generate all combinations of inserting "n" after each vowel
        for insertion in product(*[[0, 1] for _ in insertion_points]):
            modified_variation = []
            last_index = 0

            for (index, insert_pos), insert_flag in zip(insertion_points, insertion):
                modified_variation.append(variation[last_index:insert_pos])
                if insert_flag:
                    modified_variation.append("n")
                last_index = insert_pos

            modified_variation.append(variation[last_index:])
            new_variations.add("".join(modified_variation))

    prompt_var_options.update(new_variations)
    return prompt_var_options