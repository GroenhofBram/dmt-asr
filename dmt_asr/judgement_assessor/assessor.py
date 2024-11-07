import pytest
from itertools import product

@pytest.mark.unit
def calculate_assessor_judgement(prompt: str, assessor: str) -> int:
    if prompt == assessor:
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
    if assessor_no_hyphens in prompt_variations:
        return 0
    


    # n-insertions 
    

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


