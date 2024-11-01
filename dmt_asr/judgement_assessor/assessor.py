import pytest

@pytest.mark.unit
def calculate_assessor_judgement(prompt: str, assessor: str) -> int:
    assessor = assessor.replace("-","")

    print(f"Matching {prompt} , {assessor}")
    # Prompt == Assessor cases
    if prompt == assessor or prompt in assessor:
        return 0
    
    #Voicedness
    
    print("Voicedness")
    prompt_variations = generate_prompt_variations_voice(prompt)
    if assessor in prompt_variations:
        return 0

    # n-insertions 
    

    else:
        return 1
    

def generate_prompt_variations_voice(voicedness_prompt):
    # Voicedness
    voicedness_pairs = set()
    voicedness_pairs.add(("p","b"))
    voicedness_pairs.add(("t","d"))
    voicedness_pairs.add(("f","v"))
    voicedness_pairs.add(("g","k"))
    voicedness_pairs.add(("z","s"))
    
    voicedness_pairs.add(("b","p"))
    voicedness_pairs.add(("d","t"))
    voicedness_pairs.add(("v","f"))
    voicedness_pairs.add(("k","g"))
    voicedness_pairs.add(("s","z"))

    prompt_var_options = set()
    prompt_var_options.add(voicedness_prompt)

    # prompt == pink
    # pink -> bink -> 

    for voice_pairs in voicedness_pairs:
        letter = voice_pairs[0]
        replacement = voice_pairs[1]

    print(prompt_var_options)
    return prompt_var_options
